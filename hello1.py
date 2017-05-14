import pymongo,pprint,random
from flask import Flask,render_template,request,make_response
app = Flask(__name__)

connection = pymongo.MongoClient("mongodb://localhost")
db = connection.testdb1
collection = db.test_collection
users = db.users


@app.route("/")
def main_page():
    user_list=[]
    if request.cookies.get('user')!=None:
        cookie=True
    else:
        cookie=False
    content=request.cookies.get('user')
    for user in users.find():
        user_list.append((user['name'],user['id']))
    if cookie==True:
    	idx = request.cookies.get('user').find('/')
        user1 = request.cookies.get('user')[:idx]
        user1 = users.find_one({"name":user1})
        message = str(user1['message'])
    else:
        message= None
    return render_template('sample4_next2.html',users=user_list,not_cookie=(not cookie),content=content,message = message)

@app.route("/login",methods=['POST'])
def login():
    name = request.form['name']
    user = request.form['id']
    pass1 = request.form['pw']
    if users.find_one({"id":user,"pw":pass1})!=None:
        user1 = users.find_one({"id":user,"pw":pass1})
        mess = str(user1['message'])
        resp = make_response(render_template('sample4_next2.html', not_cookie=False, content=name+'/'+user, message=mess))
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
    remove1=[]
    manitto_list = []
    result = []
    check = True
    for key, value in request.form.iteritems():
        if key.find('remove')!=-1 and value != '':
            remove.append(value)
        if key.find('box')!=-1:
            manitto_list.append(key[3:].decode('utf-8'))
    for i in range(0,len(remove),2):
        temp1 = [remove[i],remove[i+1]]
        temp2 = [remove[i+1], remove[i]]
        remove1.append(temp1)
        remove1.append(temp2)
    random.shuffle(manitto_list)
    print remove1,manitto_list
    while True:
        check = True
        for i in range(len(manitto_list)-1):
            if [manitto_list[i], manitto_list[i+1]] in remove1:
                check = False
                random.shuffle(manitto_list)
                print manitto_list
        if [manitto_list[len(manitto_list)-1], manitto_list[0]] in remove1:
                check = False
                random.shuffle(manitto_list)
                print manitto_list
        if (check == True):
                break
    for i in range(len(manitto_list)-1):
                temp = [manitto_list[i], manitto_list[i+1]]
                result.append(temp)
    temp = [manitto_list[len(manitto_list)-1], manitto_list[0]]
    result.append(temp)
    #print result
    for i in range(len(result)):
        user = users.find_one({"name":result[i][0]})
        if user != None:
            print "Find someone"
            user['message'] = result[i][1]
            print user['message']
            users.save(user)
    idx = request.cookies.get('user').find('/')
    user1 = request.cookies.get('user')[:idx]
    user1 = users.find_one({"name":user1})
    message = str(user1['message'])
    content = request.cookies.get('user')
    return render_template('sample4_next2.html', content = content, not_cookie=False, message=message)

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
    #return str(user)+'\n'+str(pass1)+'\n'+str(name)
    return render_template('sample4_next2.html', not_cookie=False, content=name+'/'+user)#render_template('sample4_next2.html',not_cookie=True)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=5000)
