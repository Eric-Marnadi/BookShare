import redis
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

def appendToList(string, value):
    if(string==None):
        return value
    return string + ", " + value

def popFromList(string):
    if("," in string):
        return(string.split(",")[0], string[string.index(",") + 1::].strip())
    return(string, "")

def get_connection():
    try:
        r = redis.StrictRedis(host="localhost", port=6379, password="", decode_responses=True)
        return r
    except Exception as e:
        print(e)

connection = get_connection()

def user_exists(username):
    return(connection.exists("user/" + username))

def add_user(firstname, lastname, email, username, password):
    connection.hmset("user/" + username, {"firstname":firstname, "lastname":lastname, "email":email, "password":set_password(password)})

def check_password(username, password):
    return check_password_hash(connection.hgetall("user/" + username)["password"], password)

def request_book(bookname, isbn, username):
    id = str(uuid.uuid4())
    try:
        missing_request = connection.hget("missing/request", isbn)
        book_id, missing_request = popFromList(missing_request)
        request_row = connection.hgetall("book/" + book_id)
        print("missing/request exists")
        request_row["requester"] = "user/" + username
        connection.hmset("book/" + id, dict(request_row))
        connection.hset("missing/request", isbn, missing_request)
        print("MATCHED with " + request_row["supplier"])
    except:
        try:
            missing_supply = connection.hget("missing/supply", isbn)
            missing_supply = appendToList(missing_supply, id)
            connection.hmset("book/" + id,
                             {"name": bookname, "ISBN": isbn, "supplier": "", "requester": "user/" + username})
            connection.hset("missing/supply", isbn, missing_supply)
        except Exception as e:
            print(e)
            print("creating missing/supply")
            connection.hmset("book/" + id, {"name":bookname, "ISBN":isbn, "supplier":"","requester":"user/" + username})
            connection.hset("missing/supply", isbn, str(id))
def supply_book(bookname, isbn, username):
    id = str(uuid.uuid4())
    try:
        missing_supply = connection.hget("missing/supply", isbn)
        book_id, missing_supply = popFromList(missing_supply)
        supply_row = connection.hgetall("book/" + book_id)
        print("missing/supply exists")
        supply_row["supplier"] = "user/" + username
        connection.hmset("book/" + id, dict(supply_row))
        connection.hset("missing/supply", isbn, missing_supply)
        print("MATCHED")
    except:
        try:
            missing_request = connection.hget("missing/request", isbn)
            print("missing/request exists")
            missing_request = appendToList(missing_request, id)
            connection.hmset("book/" + id,
                             {"name": bookname, "ISBN": isbn, "supplier": "user/" + username, "requester": ""})
            connection.hset("missing/request", isbn, missing_request)
        except Exception as e:
            print(e)
            print("creating missing/request")
            connection.hmset("book/" + id, {"name":bookname, "ISBN":isbn, "supplier":"user/" + username,"requester":""})
            connection.hset("missing/request", isbn, str(id))

def set_password(password):
    password_hash = generate_password_hash(password)
    return password_hash

def get_name(username):
    return connection.hgetall("user/" + username)["firstname"]
