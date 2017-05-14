import pymongo,pprint
from flask import Flask,render_template,request
app = Flask(__name__)

connection = pymongo.MongoClient("mongodb://localhost")
db = connection.testdb
collection = db.test_collection
users = db.users


@app.route("/")
def register():
    return render_template('sample.html')

@app.route("/login",methods=['POST'])
def login():
    user = request.form['id']
    pass1 = request.form['pw']
    if users.find_one({"id":user,"pw":pass1})!=None:
        return "Login as"+user
    else:
        return "Login Failed"

@app.route("/search",methods=['POST'])
def search():
    name = request.form['name']
    if users.find_one({"name":name})!=None:
        return "Person "+name+" exists"
    else:
        return "Person Doesn't exist"

@app.route("/match",methods=['POST'])
def match():
    

@app.route("/register",methods=['POST'])
def hello_user():
    print request.form
    user = request.form['id']
    name = request.form['name']
    pass1 = request.form['pw']
    print request.form 
    user_one={"id":user,"name":name,"pw":pass1}
    if users.find_one({"name":name})==None:
    	users.insert_one(user_one)
    else:
        return "Same name already exists"
    return str(user)+'\n'+str(pass1)+'\n'+str(name)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=5001)
