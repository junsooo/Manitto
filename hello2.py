import pymongo,pprint,random
from flask import Flask,render_template,request,make_response
app = Flask(__name__)

connection = pymongo.MongoClient("mongodb://localhost")
db = connection.testdb1
collection = db.test_collection
users = db.users


@app.route("/")
def register():
    user_list=[]
    if request.cookies.get('user')!=None:
        cookie=True
    else:
        cookie=False
    content=request.cookies.get('user')
    for user in users.find():
        user_list.append((user['name'],user['id']))
    return render_template('sample4_next2.html',users=user_list,not_cookie=(not cookie),content=content)

@app.route("/login",methods=['POST'])
def login():
    name = request.form['name']
    user = request.form['id']
    pass1 = request.form['pw']
    if users.find_one({"id":user,"pw":pass1})!=None:
        resp = make_response(render_template('sample4_next2.html', not_cookie=False, content=name+'/'+user))
        resp.set_cookie('user',name+'/'+user)
        return resp
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
    remove = []
    manitto_list = []
    check = True
    for key, value in request.form.iteritems():
        if key.find('remove')!=-1 and value != '':
            remove.append(value)
        if key.find('box')!=-1:
            manitto_list.append(key[3:].decode('utf-8'))
    print remove,manitto_list
    while check:
        random.shuffle(manitto_list)
        for i in range(len(manitto_list)-1):
            for j in range(0,len(remove),2):
                if (manitto_list[i]==remove[j] and manitto_list[i+1]==remove[j+1]) or (manitto_list[i]==remove[j+1] and manitto_list[i+1]==remove[j]):
                    continue
        check=False
    print manitto_list
    return str(request.form)

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
    app.run(debug=True,host='0.0.0.0',port=5000)
