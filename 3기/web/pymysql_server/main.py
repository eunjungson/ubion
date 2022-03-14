from flask import Flask, render_template, request, redirect, url_for
from modules import mod_sql

app = Flask(__name__)

#localhost로 접속했을때
@app.route("/")
def index():
    return render_template("index.html")

#localhost/signup로 접속했을때
@app.route("/signup/", methods=["GET"])
def signup():
    return render_template("signup.html")
@app.route("/signup", methods=["POST"])
def signup_2():
    _id = request.form["_id"]
    _password = request.form["_password"]
    _name = request.form["_name"]
    _phone = request.form["_phone"]
    _gender = request.form["_gender"]
    _age = request.form["_age"]
    _ads = request.form["_ads"]
    _regitdate = request.form["_regitdate"]
    sql = """
            INSERT INTO user_info VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s)
        """
    _values = [_id, _password, _name, _phone, _ads, _gender, _age, _regitdate]
    _db = mod_sql.Database()
    _db.execute(sql, _values)
    _db.commit()
    # print(request.form)
    return redirect(url_for('index'))

@app.route("/login/", methods=["POST"])
def login():
    #DB -> SELECT문을 사용 -> index page input ID, PASSWORD 받아와서
    # SELECT문으로 조회
    # 결과 값이 존재하면 return "login" 존재하지 않으면 return "Fail"
    # index.html 수정 main.py 수정
    # 1.index.html /login url에 post형식으로 접속.
    # ID, PASSWORD print 출력
    # 2.DB에서 SELECT문을 실행해서 user_info table 정보를 print() 출력
    # 3. SELECT문에 조건식을 추가하여 데이터의 유무 판별
    _id = request.form["_id"]
    _password = request.form["_password"]
    # print(_id, _password)    #1번 완료
    sql = """
            SELECT * FROM user_info WHERE ID = %s AND password = %s
        """
    _values = [_id, _password]
    _db = mod_sql.Database()
    result = _db.executeAll(sql, _values)
    # result -> [
    # {'ID': '', 'password': '7', 'name': '8', 'phone': '9', 'ads': '6', 'gender': 4, 'age': 3, 'regit_date': '5'}, 
    # {'ID': '1234', 'password': '8', 'name': '1', 'phone': '52', 'ads': '45', 'gender': 13, 'age': 26, 'regit_date': '1'}, 
    # {'ID': '5', 'password': '1', 'name': '2', 'phone': '3', 'ads': '4', 'gender': 8, 'age': 8, 'regit_date': '9'}, 
    # {'ID': 'test', 'password': '1234', 'name': '고길동', 'phone': '01012345678', 'ads': '서울시 강북구 쌍문동', 'gender': 1, 'age': 45, 'regit_date': '20220310'}, 
    # {'ID': 'test2', 'password': '5678', 'name': '둘리', 'phone': '01098765432', 'ads': '북극 어딘가', 'gender': 1, 'age': 10, 'regit_date': '20220310'}, 
    # {'ID': 'test3', 'password': '8513', 'name': '마이콜', 'phone':'01048426489', 'ads': '고길동 옆 집', 'gender': 1, 'age': 28, 'regit_date': '20000220310'}, 
    # {'ID': 'test4', 'password': '4521', 'name': '또치', 'phone': '01051247856', 'ads': '동물원', 'gender': 2, 'age': 4, 'regit_date': '20200310'}, 
    # {'ID': 'test5', 'password': '5555', 'name': '도우너', 'phone': '01012345678', 'ads': '깐따삐아', 'gender': 1, 'age': 10, 'regit_date': '20220310'}, 
    # {'ID': 'test6', 'password': '1111', 'name': '희동이', 'phone': '01012345678', 'ads': '고길동집', 'gender': 1, 'age': 3, 'regit_date': '20220311'}
    # ]
    # list 형태에서 [1,2,3,4] -> 1을 출력하려면 ? list[0] -> 1출력
    # dict = [{name:1},{name:2},{name:3}] -> {name:1}을 출력하려면? -> dict[0] = {name:1}
    # 1을 출력하려면? -> dict[0]["name"]-> 1


    print(request.query_string)   #2번 완료

    if result:
        return render_template("welcome.html", 
                                name = result[0]["name"], 
                                id = result[0]["ID"])
    else : 
        return redirect(url_for('index'))

    # return redirect(url_for('index'))

@app.route("/update", methods=["GET"])
def update():
    id = request.args["_id"]
    sql = """
            SELECT * FROM user_info WHERE ID = %s
        """
    values = [id]
    _db = mod_sql.Database()
    result = _db.executeAll(sql, values)
    return render_template("update.html", info = result[0])
@app.route("/update", methods=["POST"])
def update_2():
    _id = request.form["_id"]
    _password = request.form["_password"]
    _name = request.form["_name"]
    _phone = request.form["_phone"]
    _gender = request.form["_gender"]
    _age = request.form["_age"]
    _ads = request.form["_ads"]
    sql = """
            UPDATE user_info SET 
            password = %s, 
            name = %s, 
            phone = %s,
            gender = %s, 
            age = %s, 
            ads = %s
            WHERE ID = %s
        """
    values = [_password, _name, _phone, _gender, _age, _ads, _id]
    _db = mod_sql.Database()
    _db.execute(sql, values)
    _db.commit()
    return redirect(url_for('index'))


app.run(port=8080, debug=True)