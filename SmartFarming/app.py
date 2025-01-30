import random
from functools import wraps

from flask import *
from DBConnection import *

app = Flask(__name__)
app.secret_key = "MY_SECRET_KEY"
static_path = "C:\\Users\\ROCK\\Downloads\\CP\\Python\\SmartFarming"


# def login_required(f):
#     @wraps(f)
#     def wrap(*args, **kwargs):
#         if session['lid'] is not None:
#             flash("You need to login first")
#             return login_page()
#         else:
#             return f(*args, **kwargs)
#     return wrap


@app.route('/home')
def home_page():  # put application's code here
    return render_template('home.html')


@app.route('/')
@app.route('/login')
def login_page():
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/login_post', methods=['post'])
def login_page_post():
    username = request.form['name']
    password = request.form['pass']
    qry = f"select * from login where uname='{username}' and password='{password}'"
    db = Db()
    res = db.selectOne(qry)
    if res is None:
        return '''<script>alert('invalid');window.location='/login'</script>'''
    elif res['type'] == 'admin':
        session['lid'] = res['loginid']
        return redirect('/home')
    elif res['type'] == 'tech_wing':
        session['lid'] = res['loginid']
        return redirect('/wing_home')
    elif res['type'] == 'agriculture_officer':
        session['lid'] = res['loginid']
        return redirect('/ao_home')
    else:
        return '''<script>alert('invalid');window.location='/login'</script>'''


@app.route('/change_password')
# @login_required
def change_password():
    return render_template("change_password.html")


@app.route('/change_password_post', methods=['POST'])
def change_password_post():
    db = Db()
    id = str(session['lid'])
    password = request.form['pass']
    confirm = request.form['confirm_pass']
    current_pass = request.form['current_pass']
    qry = "select * from login where loginid='" + id + "'"
    res = db.selectOne(qry)
    if res['password'] == current_pass:
        if password == confirm:

            qry = "UPDATE login SET password='" + password + "' where loginid='" + id + "'"
            db.update(qry)
            return '''<script>alert('Password Updated Successfully');window.location='/login'</script> '''
        else:
            return '''<script>alert('passwords is not matching');window.location='/change_password'</script> '''
    else:
        return '''<script>alert('old pass is not matching');window.location='/change_password'</script> '''


# ---------------------
# ADD SECTION
# ---------------------


@app.route('/add_agri_offi')
def add_agri_offi_page():
    return render_template('add_agri_offi.html')


@app.route('/add_agri_offi_post', methods=['post'])
def add_agri_offi_page_post():
    name = request.form['name']
    gender = request.form['gender']
    dob = request.form['dob']
    phone = request.form['pn']
    email = request.form['email']
    house_name = request.form['hname']
    place = request.form['place']
    city = request.form['city']
    district = request.form['district']
    state = request.form['state']
    pincode = request.form['pin']
    photo = request.files['photo']
    from datetime import datetime
    file = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
    photo.save(static_path + "\\agriofficer\\" + file)
    fname = "/static/agriofficer/" + file
    password = random.randint(0000, 9999)
    db = Db()
    qry = "INSERT INTO login VALUES('','" + email + "','" + str(password) + "','agriculture_officer')"
    res = db.insert(qry)
    qry1 = "INSERT INTO agriculture_officer VALUES ('','" + str(
        res) + "','" + name + "', '" + gender + "', '" + dob + "', '" + email + "', '" + phone + "', '" + house_name + "', '" + place + "', '" + city + "', '" + district + "', '" + state + "', '" + pincode + "', '" + fname + "')"
    res1 = db.insert(qry1)
    return "Added!"


@app.route('/add_crop')
def add_crop_page():
    return render_template("add_crop.html")


@app.route('/add_crop_post', methods=['post'])
def add_crop_page_post():
    name = request.form['name']
    desc = request.form['desc']
    photo = request.files['photo']
    from datetime import datetime
    file = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
    photo.save(static_path + "\\crop\\" + file)
    fname = "/static/crop/" + file
    qry = "INSERT INTO crop VALUES ('','" + name + "','" + desc + "','" + fname + "')"
    db = Db()
    db.insert(qry)
    return "Success"


@app.route('/add_equipment')
def add_equipment_page():
    return render_template('add_equipment.html')


@app.route('/add_equipment_post', methods=['post'])
def add_equipment_page_post():
    name = request.form['name']
    photo = request.files['photo']
    desc = request.form['desc']
    from datetime import datetime
    file = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
    photo.save(static_path + "\\equipments\\" + file)
    fname = "/static/equipments/" + file
    price = request.form['price']
    qry = "INSERT INTO equipment_machine VALUES ('','" + name + "','" + fname + "','" + desc + "', '" + price + "')"
    db = Db()
    db.insert(qry)
    return f"Success\n\tName:{name}"


@app.route('/add_f_p')
def add_fertiliser_pesticide():
    return render_template('add_ferti_pesti.html')


@app.route('/add_f_p_post', methods=['post'])
def add_fertiliser_pesticide_post():
    name = request.form['name']
    photo = request.files['photo']
    from datetime import datetime
    file = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
    photo.save(static_path + "\\ferti_pesti\\" + file)
    fname = "/static/ferti_pesti/" + file
    desc = request.form['desc']
    howtouse = request.form['howtouse']
    qry = "INSERT INTO ferti_pesticide VALUES ('', '" + name + "', '" + fname + "', '" + desc + "', '" + howtouse + "')"
    db = Db()
    db.insert(qry)
    return f"Success\n\tName:{name}"


@app.route('/add_message')
def add_message():
    return render_template('add_message.html')


@app.route('/add_message_post', methods=['post'])
def add_message_post():
    sub = request.form['subject']
    date = request.form['date']
    message = request.form['message']
    qry = "INSERT INTO message values ('','" + sub + "','" + message + "','" + date + "')"
    db = Db()
    db.insert(qry)
    return sub


@app.route('/add_tech_wing')
def add_tech_wing_page():
    return render_template('add_tech_wing.html')


@app.route('/add_tech_wing_post', methods=['post'])
def add_tech_wing_page_post():
    name = request.form['name']
    gender = request.form['gender']
    dob = request.form['dob']
    phone = request.form['pn']
    email = request.form['email']
    house_name = request.form['hname']
    place = request.form['place']
    city = request.form['city']
    district = request.form['district']
    state = request.form['state']
    pincode = request.form['pin']
    photo = request.files['photo']
    from datetime import datetime
    file = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
    photo.save(static_path + "\\tech_wing\\" + file)
    fname = "/static/tech_wing/" + file
    password = random.randint(0000, 9999)
    db = Db()
    qry = "INSERT INTO login VALUES('','" + email + "','" + str(password) + "','tech_wing')"
    res = db.insert(qry)
    qry1 = "INSERT INTO technical_wing VALUES ('','" + str(
        res) + "','" + name + "', '" + gender + "', '" + dob + "', '" + email + "', '" + phone + "', '" + house_name + "', '" + place + "', '" + city + "', '" + district + "', '" + state + "', '" + pincode + "', '" + fname + "')"
    res1 = db.insert(qry1)

    return "Added!"


@app.route('/add_group_policy')
def add_group_policy():
    return render_template('add_group_policy.html')


@app.route('/add_group_policy_post', methods=['post'])
def add_group_policy_page_post():
    name = request.form['name']
    pfile = request.files['pfile']
    from datetime import datetime
    file = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
    pfile.save(static_path + "\\group_policy\\" + file)
    fname = "/static/group_policy/" + file
    date = request.form['date']
    desc = request.form['desc']
    qry = f"INSERT INTO group_policy VALUES ('', '{name}', '{fname}', '{date}', '{desc}')"
    db = Db()
    db.insert(qry)
    return name


# ---------------------
# EDIT SECTION
# ---------------------

@app.route('/view_agri_offi')
def view_agri_offi():
    qry = "SELECT * FROM agriculture_officer"
    db = Db()
    res = db.select(qry)
    return render_template('view_agri_offi.html', data=res)


@app.route('/view_agri_offi_post', methods=['POST'])
def view_agri_offi_post():
    name = request.form['name']
    qry = "SELECT * FROM agriculture_officer WHERE NAME LIKE '%" + name + "%'"
    db = Db()
    res = db.select(qry)
    return render_template('view_agri_offi.html', data=res)


@app.route('/view_complaint')
def view_complaint():
    qry = "SELECT complaint.*,user.* FROM complaint JOIN USER ON user.ulid=complaint.lid"
    db = Db()
    res = db.select(qry)
    return render_template('view_complaint.html', data=res)


@app.route('/view_complaint_post', methods=['post'])
def view_complaint_post():
    from_date = request.form['from']
    to_date = request.form['to']
    db = Db()
    qry = "SELECT complaint.*,user.* FROM complaint JOIN USER ON user.ulid=complaint.lid WHERE date between '" + from_date + "' and '" + to_date + "'"
    res = db.select(qry)
    return render_template('view_complaint.html', data=res)


@app.route('/view_crop')
def view_crop():
    qry = "SELECT * FROM crop"
    db = Db()
    res = db.select(qry)
    return render_template('view_crop.html', data=res)


@app.route('/view_crop_post', methods=['post'])
def view_crop_post():
    name = request.form['name']
    qry = f"SELECT * FROM crop WHERE name LIKE '%{name}%'"
    db = Db()
    res = db.select(qry)
    return render_template('view_crop.html', data=res)


@app.route('/view_equipment')
def view_equipment():
    qry = "SELECT * FROM equipment_machine"
    db = Db()
    res = db.select(qry)
    return render_template('view_equipment.html', data=res)


@app.route('/view_equipment_post', methods=['POST'])
def view_equipment_post():
    name = request.form['name']
    qry = f"SELECT * FROM equipment_machine WHERE equipment_name LIKE '%{name}%'"
    db = Db()
    res = db.select(qry)
    return render_template('view_equipment.html', data=res)


@app.route('/view_feedback')
def view_feedback():
    db = Db()
    qry = "SELECT feedback.*,user.* FROM feedback JOIN USER ON user.ulid=feedback.ulid"
    res = db.select(qry)
    return render_template('view_feedback.html', data=res)


@app.route('/view_feedback_post', methods=['post'])
def view_feedback_post():
    from_date = request.form['from']
    to_date = request.form['to']
    db = Db()
    qry = "SELECT feedback.*,user.* FROM feedback JOIN USER ON user.ulid=feedback.ulid WHERE date between '" + from_date + "' and '" + to_date + "'"
    res = db.select(qry)
    print(res)
    return render_template('view_feedback.html', data=res)


@app.route('/view_ferti_pesti')
def view_ferti_pesti():
    qry = "SELECT * from ferti_pesticide"
    db = Db()
    res = db.select(qry)
    return render_template('view_ferti_pesti.html', data=res)


@app.route('/view_ferti_pesti_post', methods=['POST'])
def view_ferti_pesti_post():
    name = request.form['name']
    qry = f"SELECT * from ferti_pesticide where name like '%{name}%'"
    db = Db()
    res = db.select(qry)
    return render_template('view_ferti_pesti.html', data=res)


@app.route('/view_notification')
def view_notification():
    db = Db()
    qry = "SELECT * FROM notification"
    res = db.select(qry)
    return render_template('view_notification.html', data=res)


@app.route('/view_notification_post', methods=['POST'])
def view_notification_post():
    name = request.form['name']
    db = Db()
    qry = f"SELECT * FROM notification WHERE subject LIKE '%{name}%'"
    res = db.select(qry)
    return render_template('view_notification.html', data=res)


@app.route('/view_policy')
def view_policy():
    qry = "select * from group_policy"
    db = Db()
    res = db.select(qry)
    return render_template('view_policy.html', data=res)


@app.route('/view_policy_post', methods=['POST'])
def view_policy_post():
    name = request.form['name']
    qry = f"select * from group_policy where policy_name like '%{name}%'"
    db = Db()
    res = db.select(qry)
    return render_template('view_policy.html', data=res)


@app.route('/view_tech_wing')
def view_tech_wing():
    qry = "select * from technical_wing"
    db = Db()
    res = db.select(qry)
    return render_template('view_tech_wing.html', data=res)


@app.route('/view_tech_wing_post', methods=['POST'])
def view_tech_wing_post():
    name = request.form['name']
    qry = f"select * from technical_wing where name like '%{name}%'"
    db = Db()
    res = db.select(qry)
    return render_template('view_tech_wing.html', data=res)


@app.route('/view_user')
def view_user():
    qry = "select * from user"
    db = Db()
    res = db.select(qry)
    return render_template('view_user.html', data=res)


@app.route('/view_user_post', methods=['POST'])
def view_user_post():
    name = request.form['name']
    qry = f"select * from user where name like '%{name}%'"
    db = Db()
    res = db.select(qry)
    return render_template('view_user.html', data=res)


@app.route('/send_reply/<id>')
def send_reply(id):
    db = Db()
    qry = "select * from complaint where complaintid='" + id + "'"
    res = db.selectOne(qry)
    return render_template('send_reply.html', data=res)


@app.route('/send_reply_post', methods=['POST'])
def send_reply_post():
    id = request.form['id']
    reply = request.form['reply']
    db = Db()
    qry = "UPDATE complaint SET reply='" + reply + "',status='completed' WHERE complaintid='" + id + "'"
    db.update(qry)
    return view_complaint()


# ---------------------
# EDIT SECTION
# ---------------------

@app.route('/edit_agri_offi/<id>')
def edit_agri_offi_page(id):
    db = Db()
    qry = f"SELECT * FROM agriculture_officer WHERE agri_officer_id='{id}'"
    res = db.selectOne(qry)
    return render_template('edit_agri_offi.html', data=res)


@app.route('/edit_agri_offi_post', methods=['post'])
def edit_agri_offi_page_post():
    db = Db()
    id = request.form['id']
    name = request.form['name']
    gender = request.form['gender']
    dob = request.form['dob']
    phone = request.form['pn']
    email = request.form['email']
    house_name = request.form['hname']
    place = request.form['place']
    city = request.form['city']
    district = request.form['district']
    state = request.form['state']
    pincode = request.form['pin']
    if 'photo' in request.files:
        photo = request.files['photo']
        from datetime import datetime
        file = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
        photo.save(static_path + "\\agriofficer\\" + file)
        fname = "/static/agriofficer/" + file
        if photo.filename != "":
            qry = f"UPDATE agriculture_officer SET name='{name}',gender='{gender}',dob='{dob}',email='{email}',phone='{phone}',hno_name='{house_name}',place='{place}',city='{city}',district='{district}',state='{state}',pincode='{pincode}',photo='{fname}' where agri_officer_id='{id}'"
            res = db.update(qry)
            return view_agri_offi()
        else:
            qry = f"UPDATE agriculture_officer SET name='{name}',gender='{gender}',dob='{dob}',email='{email}',phone='{phone}',hno_name='{house_name}',place='{place}',city='{city}',district='{district}',state='{state}',pincode='{pincode}' where agri_officer_id='{id}'"
            res = db.update(qry)
            return view_agri_offi()
    else:
        qry = f"UPDATE agriculture_officer SET name='{name}',gender='{gender}',dob='{dob}',email='{email}',phone='{phone}',hno_name='{house_name}',place='{place}',city='{city}',district='{district}',state='{state}',pincode='{pincode}' where agri_officer_id='{id}'"
        res = db.update(qry)
        return view_agri_offi()


@app.route('/edit_crop/<id>')
def edit_crop_page(id):
    db = Db()
    qry = f"SELECT * FROM crop WHERE cropid='{id}'"
    res = db.selectOne(qry)
    return render_template("edit_crop.html", data=res)


@app.route('/edit_crop_post', methods=['post'])
def edit_crop_page_post():
    db = Db()
    id = request.form['id']
    name = request.form['name']
    desc = request.form['desc']
    if 'photo' in request.files:
        photo = request.files['photo']
        from datetime import datetime
        file = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
        photo.save(static_path + "\\crop\\" + file)
        fname = "/static/crop/" + file
        if photo.filename != "":
            qry = f"UPDATE crop SET name='{name}',details='{desc}',photo='{fname}' WHERE cropid='{id}'"
            res = db.update(qry)
            return view_crop()
        else:
            qry = f"UPDATE crop SET name='{name}',details='{desc}' WHERE cropid='{id}'"
            res = db.update(qry)
            return view_crop()
    else:
        qry = f"UPDATE crop SET name='{name}',details='{desc}' WHERE cropid='{id}'"
        res = db.update(qry)
        return view_crop()


@app.route('/edit_equipment/<id>')
def edit_equipment_page(id):
    db = Db()
    qry = f"SELECT * FROM equipment_machine WHERE ea_ma_id='{id}'"
    res = db.selectOne(qry)
    return render_template('edit_equipment.html', data=res)


@app.route('/edit_equipment_post', methods=['post'])
def edit_equipment_page_post():
    db = Db()
    id = request.form['id']
    name = request.form['name']
    desc = request.form['desc']
    price = request.form['price']
    if 'photo' in request.files:
        photo = request.files['photo']
        from datetime import datetime
        file = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
        photo.save(static_path + "\\equipments\\" + file)
        fname = "/static/equipments/" + file
        if photo.filename != "":
            qry = f"UPDATE equipment_machine SET equipment_name='{name}',description='{desc}',price='{price}',photo='{fname}' WHERE ea_ma_id='{id}'"
            res = db.update(qry)
            return view_equipment()
        else:
            qry = f"UPDATE equipment_machine SET equipment_name='{name}',description='{desc}',price='{price}' WHERE ea_ma_id='{id}'"
            res = db.update(qry)
            return view_equipment()
    else:
        qry = f"UPDATE equipment_machine SET equipment_name='{name}',description='{desc}',price='{price}' WHERE ea_ma_id='{id}'"
        res = db.update(qry)
        return view_equipment()


@app.route('/edit_f_p/<id>')
def edit_fertiliser_pesticide(id):
    db = Db()
    qry = f"SELECT * FROM ferti_pesticide WHERE fpid='{id}'"
    res = db.selectOne(qry)
    return render_template('edit_ferti_pesti.html', data=res)


@app.route('/edit_f_p_post', methods=['post'])
def edut_fertiliser_pesticide_post():
    db = Db()
    id = request.form['id']
    name = request.form['name']
    desc = request.form['desc']
    howtouse = request.form['howtouse']
    if 'photo' in request.files:
        photo = request.files['photo']
        from datetime import datetime
        file = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
        photo.save(static_path + "\\ferti_pesti\\" + file)
        fname = "/static/ferti_pesti/" + file
        if photo.filename != "":
            qry = f"UPDATE ferti_pesticide SET name='{name}',description='{desc}',how_to_use='{howtouse}',photo='{fname}' WHERE fpid='{id}'"
            res = db.update(qry)
            return view_ferti_pesti()
        else:
            qry = f"UPDATE ferti_pesticide SET name='{name}',description='{desc}',how_to_use='{howtouse}' WHERE fpid='{id}'"
            res = db.update(qry)
            return view_ferti_pesti()
    else:
        qry = f"UPDATE ferti_pesticide SET name='{name}',description='{desc}',how_to_use='{howtouse}' WHERE fpid='{id}'"
        res = db.update(qry)
        return view_ferti_pesti()


@app.route('/edit_message/<id>')
def edit_message(id):
    db = Db()
    qry = f"SELECT * FROM message WHERE messageid='{id}'"
    res = db.selectOne(qry)
    return render_template('edit_message.html', data=res)


# @app.route('/edit_message_post', methods=['post'])
# def edit_message_post():
#     sub = request.form['subject']
#     date = request.form['date']
#     message = request.form['message']
#     qry = "INSERT INTO message values ('','" + sub + "','" + message + "','" + date + "')"
#     db = Db()
#     db.insert(qry)
#     return sub


@app.route('/edit_tech_wing/<id>')
def edit_tech_wing_page(id):
    db = Db()
    qry = f"SELECT * FROM technical_wing WHERE wingid='{id}'"
    res = db.selectOne(qry)
    return render_template('edit_tech_wing.html', data=res)


@app.route('/edit_tech_wing_post', methods=['post'])
def edit_tech_wing_page_post():
    db = Db()
    id = request.form['id']
    name = request.form['name']
    gender = request.form['gender']
    dob = request.form['dob']
    phone = request.form['pn']
    email = request.form['email']
    house_name = request.form['hname']
    place = request.form['place']
    city = request.form['city']
    district = request.form['district']
    state = request.form['state']
    pincode = request.form['pin']
    if 'photo' in request.files:
        photo = request.files['photo']
        from datetime import datetime
        file = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
        photo.save(static_path + "\\tech_wing\\" + file)
        fname = "/static/tech_wing/" + file
        if photo.filename != "":
            qry = f"UPDATE technical_wing SET name='{name}',gender='{gender}',dob='{dob}',email='{email}',phone='{phone}',hno_name='{house_name}',place='{place}',city='{city}',district='{district}',state='{state}',pincode='{pincode}',photo='{fname}' where wingid='{id}'"
            res = db.update(qry)
            return view_tech_wing()
        else:
            qry = f"UPDATE technical_wing SET name='{name}',gender='{gender}',dob='{dob}',email='{email}',phone='{phone}',hno_name='{house_name}',place='{place}',city='{city}',district='{district}',state='{state}',pincode='{pincode}' where wingid='{id}'"
            res = db.update(qry)
            return view_tech_wing()
    else:
        qry = f"UPDATE technical_wing SET name='{name}',gender='{gender}',dob='{dob}',email='{email}',phone='{phone}',hno_name='{house_name}',place='{place}',city='{city}',district='{district}',state='{state}',pincode='{pincode}' where wingid='{id}'"
        res = db.update(qry)
        return view_tech_wing()


@app.route('/edit_group_policy/<id>')
def edit_group_policy(id):
    db = Db()
    qry = f"SELECT * FROM group_policy WHERE policyid='{id}'"
    res = db.selectOne(qry)
    return render_template('edit_group_policy.html', data=res)


@app.route('/edit_group_policy_post', methods=['post'])
def edit_group_policy_page_post():
    db = Db()
    id = request.form['id']
    name = request.form['name']
    date = request.form['date']
    desc = request.form['desc']
    if 'pfile' in request.files:
        pfile = request.files['pfile']
        from datetime import datetime
        file = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
        pfile.save(static_path + "\\group_policy\\" + file)
        fname = "/static/group_policy/" + file
        if pfile.filename != "":
            qry = f"UPDATE group_policy SET policy_name='{name}',date='{date}',description='{desc}',policy_file='{fname}' WHERE policyid='{id}'"
            res = db.update(qry)
            return view_policy()
        else:
            qry = f"UPDATE group_policy SET policy_name='{name}',date='{date}',description='{desc}' WHERE policyid='{id}'"
            res = db.update(qry)
            return view_policy()
    else:
        qry = f"UPDATE group_policy SET policy_name='{name}',date='{date}',description='{desc}' WHERE policyid='{id}'"
        res = db.update(qry)
        return view_policy()


# ---------------------
# DELETE SECTION
# ---------------------

@app.route('/delete_agri_offi/<id>')
def delete_agri_offi_page(id):
    db = Db()
    qry = f"DELETE FROM agriculture_officer WHERE agri_officer_id='{id}'"
    res = db.delete(qry)
    return view_agri_offi()


@app.route('/delete_crop/<id>')
def delete_crop_page(id):
    db = Db()
    qry = f"DELETE FROM crop WHERE cropid='{id}'"
    res = db.delete(qry)
    return view_crop()


@app.route('/delete_equipment/<id>')
def delete_equipment_page(id):
    db = Db()
    qry = f"DELETE FROM equipment_machine WHERE ea_ma_id='{id}'"
    res = db.delete(qry)
    return view_equipment()


@app.route('/delete_f_p/<id>')
def delete_fertiliser_pesticide(id):
    db = Db()
    qry = f"DELETE FROM ferti_pesticide WHERE fpid='{id}'"
    res = db.delete(qry)
    return view_ferti_pesti()


@app.route('/delete_tech_wing/<id>')
def delete_tech_wing_page(id):
    db = Db()
    qry = f"DELETE FROM technical_wing WHERE wingid='{id}'"
    res = db.delete(qry)
    return view_tech_wing()


@app.route('/delete_group_policy/<id>')
def delete_group_policy(id):
    db = Db()
    qry = f"DELETE FROM group_policy WHERE policyid='{id}'"
    res = db.delete(qry)
    return view_policy()


@app.route('/delete_notification/<id>')
def delete_notification(id):
    db = Db()
    qry = f"DELETE FROM notification WHERE notificationid='{id}'"
    res = db.delete(qry)
    return view_notification()


# Technical Wing

@app.route('/wing_home')
def wing_home():
    return render_template('tech_wing/home.html')


@app.route('/wing_view_profile')
def wing_view_profile():
    db = Db()
    qry = f"SELECT * FROM `technical_wing` WHERE `loginid`='{str(session['lid'])}'"
    res = db.selectOne(qry)
    return render_template('tech_wing/view_profile.html', data=res)


@app.route('/wing_view_farmers')
def wing_view_farmers():
    return render_template('tech_wing/view_farmers.html')


@app.route('/wing_view_idea')
def wing_view_idea():
    db = Db()
    qry = "SELECT * FROM `ideas` WHERE `technical_lid`='" + str(session['lid']) + "'"
    res = db.select(qry)
    return render_template('tech_wing/view_idea.html', data=res)


@app.route('/wing_add_idea')
def wing_add_idea():
    return render_template('tech_wing/add_idea.html')


@app.route('/wing_add_idea_post', methods=['POST'])
def wing_add_idea_post():
    subject = request.form['subject']
    details = request.form['details']
    db = Db()
    qry = "INSERT INTO `ideas`(`idea_subject`,`idea_details`,`technical_lid`) VALUES ('" + subject + "','" + details + "','" + str(
        session['lid']) + "')"
    res = db.insert(qry)
    return redirect('/wing_home')


@app.route('/wing_delete_idea/<id>')
def wing_delete_idea(id):
    db = Db()
    qry = "DELETE FROM `ideas` WHERE `ideaid`='" + id + "'"
    db.delete(qry)
    return redirect('/wing_view_idea')


@app.route('/wing_edit_idea/<id>')
def wing_edit_idea(id):
    db = Db()
    qry = "SELECT * FROM `ideas` WHERE `ideaid`='" + id + "'"
    res = db.selectOne(qry)
    return render_template('tech_wing/edit_idea.html', data=res)


@app.route('/wing_edit_idea_post', methods=['POST'])
def wing_edit_idea_post():
    idea_id = request.form['id']
    subject = request.form['subject']
    details = request.form['details']
    db = Db()
    qry = "UPDATE `ideas` SET `idea_subject`='" + subject + "',`idea_details`='" + details + "' WHERE `ideaid`='" + idea_id + "'"
    db.update(qry)
    return redirect('/wing_home')


@app.route('/wing_add_techniques')
def wing_add_techniques():
    return render_template('tech_wing/add_techniques.html')


@app.route('/wing_add_techniques_post', methods=['POST'])
def wing_add_techniques_post():
    name = request.form['name']
    date = request.form['date']
    desc = request.form['desc']
    photo = request.files['photo']
    from datetime import datetime
    file = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
    photo.save(static_path + "wing_techniques\\" + file)
    fname = "/static/wing_techniques/" + file
    db = Db()
    qry = "INSERT INTO `techniques` (`technical_lid`,`technique_name`,`photo`,`description`,`date`) VALUES ('" + str(
        session['lid']) + "','" + name + "','" + fname + "','" + desc + "','" + date + "')"
    res = db.insert(qry)
    print("ADDED")
    return redirect('/wing_home')


@app.route('/wing_view_techniques')
def wing_view_techniques():
    db = Db()
    qry = "SELECT * FROM `techniques` WHERE `technical_lid`='" + str(session['lid']) + "'"
    res = db.select(qry)
    return render_template('tech_wing/view_techniques.html', data=res)


@app.route('/wing_delete_techniques/<id>')
def wing_delete_techniques(id):
    db = Db()
    qry = "DELETE FROM `techniques` WHERE `technique_id`='" + id + "'"
    db.delete(qry)
    return wing_view_techniques()


@app.route('/wing_edit_techniques/<id>')
def wing_edit_techniques(id):
    db = Db()
    qry = f"SELECT * FROM `techniques` WHERE `technique_id`='{id}'"
    res = db.selectOne(qry)
    return render_template('tech_wing/edit_techniques.html', data=res)


@app.route('/wing_edit_techniques_post', methods=['POST'])
def wing_edit_techniques_post():
    db = Db()
    id = request.form['id']
    name = request.form['name']
    date = request.form['date']
    desc = request.form['desc']
    photo = request.files['photo']
    if 'photo' in request.files:
        from datetime import datetime
        file = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
        photo.save(static_path + "wing_techniques\\" + file)
        fname = "/static/wing_techniques/" + file
        if photo.filename != "":
            qry = f"UPDATE `techniques` SET `technique_name`='{name}',`photo`='{fname}',`description`='{desc}',`date`='{date}' WHERE `technique_id`='{id}'"
            db.update(qry)
            return wing_view_techniques()
        else:
            qry = f"UPDATE `techniques` SET `technique_name`='{name}',`description`='{desc}',`date`='{date}' WHERE `technique_id`='{id}'"
            db.update(qry)
            return wing_view_techniques()
    else:
        qry = f"UPDATE `techniques` SET `technique_name`='{name}',`description`='{desc}',`date`='{date}' WHERE `technique_id`='{id}'"
        db.update(qry)
        return wing_view_techniques()


@app.route('/wing_add_success_stories')
def wing_add_success_stories():
    return render_template('tech_wing/add_success_stories.html')


@app.route('/wing_add_success_stories_post', methods=['POST'])
def wing_add_success_stories_post():
    from datetime import datetime
    db = Db()
    name = request.form['name']
    subject = request.form['subject']
    desc = request.form['desc']
    upload_date = datetime.now().strftime("%Y-%m-%d")
    photo = request.files['photo']
    from datetime import datetime
    file = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
    photo.save(static_path + "wing_success_stories\\" + file)
    fname = "/static/wing_success_stories/" + file
    qry = f"INSERT INTO `success_stories` (`name`,`subject`,`photo`,`description`,`upload_date`) VALUES ('{name}','{subject}','{fname}','{desc}','{upload_date}')"
    db.insert(qry)
    return redirect('/wing_home')


@app.route('/wing_view_success_stories')
def wing_view_success_stories():
    db = Db()
    qry = "SELECT * FROM `success_stories`"
    res = db.select(qry)
    return render_template('tech_wing/view_success_stories.html', data=res)


@app.route('/wing_edit_success_stories/<id>')
def wing_edit_success_stories(id):
    db = Db()
    qry = "SELECT * FROM `success_stories` WHERE `story_id`='" + id + "'"
    res = db.selectOne(qry)
    return render_template('tech_wing/edit_success_stories.html', data=res)


@app.route('/wind_edit_success_stories_post', methods=['POST'])
def wind_edit_success_stories_post():
    db = Db()
    id = request.form['id']
    name = request.form['name']
    subject = request.form['subject']
    desc = request.form['desc']
    if 'photo' in request.files:
        photo = request.files['photo']
        from datetime import datetime
        file = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
        photo.save(static_path + "wing_success_stories\\" + file)
        fname = "/static/wing_success_stories/" + file
        if photo.filename != "":
            qry = f"UPDATE `success_stories` SET `name`='{name}',`subject`='{subject}',`photo`='{fname}',`description`='{desc}' WHERE `story_id`='{id}'"
            db.update(qry)
            return wing_view_success_stories()
        else:
            qry = f"UPDATE `success_stories` SET `name`='{name}',`subject`='{subject}',`description`='{desc}' WHERE `story_id`='{id}'"
            db.update(qry)
            return wing_view_success_stories()
    else:
        qry = f"UPDATE `success_stories` SET `name`='{name}',`subject`='{subject}',`description`='{desc}' WHERE `story_id`='{id}'"
        db.update(qry)
        return wing_view_success_stories()


@app.route('/wing_delete_success_stories/<id>')
def wing_delete_success_stories(id):
    db = Db()
    qry = "DELETE FROM `success_stories` WHERE `story_id`='" + id + "'"
    db.delete(qry)
    return wing_view_success_stories()


# ao --> agriculture_officer


@app.route('/ao_home')
def ao_home():
    return render_template('ao/home.html')


@app.route('/ao_view_profile')
def ao_view_profile():
    db = Db()
    qry = f"SELECT * FROM `agriculture_officer` WHERE `loginid`='{str(session['lid'])}'"
    res = db.selectOne(qry)
    return render_template('ao/view_profile.html', data=res)


@app.route('/ao_add_notification')
def ao_add_notification():
    return render_template('ao/add_notification.html')


@app.route('/ao_add_notification_post', methods=['POST'])
def ao_add_notification_post():
    from datetime import datetime
    from_id = str(session['lid'])
    subject = request.form['subject']
    message = request.form['message']
    date = datetime.now().strftime("%Y-%m-%d")
    db = Db()
    qry = f"INSERT INTO `notification`(`fromid`,`subject`,`message`,`date`) VALUES ('{from_id}','{subject}','{message}','{date}')"
    db.insert(qry)
    return ao_home()


@app.route('/ao_view_stock_of_machines_equipments')
def ao_view_stock_of_machines_equipments():
    db = Db()
    qry = "SELECT equipment_machine.*,equipment_machine_stock.* FROM `equipment_machine` JOIN `equipment_machine_stock` ON equipment_machine.ea_ma_id=equipment_machine_stock.eq_ma_id"
    res = db.select(qry)
    print(res)
    return render_template('ao/view_stock_of_machines and equipments.html', data=res)


@app.route('/ao_view_equipments')
def ao_view_equipments():
    qry = "SELECT * FROM equipment_machine"
    db = Db()
    res = db.select(qry)
    return render_template('ao/view_equipments.html', data=res)


@app.route('/ao_stock_update/<id>')
def ao_stock_update(id):
    db = Db()
    qry = f"SELECT * FROM `equipment_machine_stock` WHERE `eq_ma_id`='{id}'"
    res = db.selectOne(qry)
    return render_template('ao/stock_update.html', data=res)


@app.route('/ao_add_stock/<id>')
def ao_add_stock(id):
    db = Db()
    qry = f"SELECT * FROM `equipment_machine` WHERE `ea_ma_id`='{id}'"
    res = db.selectOne(qry)
    return render_template('ao/ao_stock_add.html', data=res)


@app.route('/ao_add_stock_post', methods=['POST'])
def ao_add_stock_post():
    id = request.form['id']
    quantity = request.form['quantity']
    db = Db()
    qry = "INSERT INTO `equipment_machine_stock` (`eq_ma_id`,`quantity`,`agriculture_lid`) VALUES ('" + id + "','" + quantity + "','" + str(
        session['lid']) + "')"
    db.insert(qry)
    return ao_view_stock_of_machines_equipments()


@app.route('/ao_stock_update_post', methods=['POST'])
def ao_stock_update_post():
    id = request.form['id']
    quantity = request.form['quantity']
    db = Db()
    qry1 = "SELECT * FROM `equipment_machine_stock` WHERE `eq_ma_id`='" + id + "' AND `agriculture_lid`='" + str(
        session['lid']) + "'"
    res1 = db.selectOne(qry1)
    if res1 is not None:
        qry = f"UPDATE `equipment_machine_stock` SET `quantity`='{quantity}' WHERE `eq_ma_id`='{id}' "
        db.update(qry)
    else:
        ao_add_stock(id)
    return ao_view_stock_of_machines_equipments()


@app.route('/ao_view_equipment_requests')
def ao_view_equipment_requests():
    db = Db()
    qry = "SELECT `request_equipment_machine`.*,`equipment_machine`.`ea_ma_id`,`equipment_machine`.`equipment_name`,`equipment_machine`.`photo`,`user`.`ulid`,`user`.`name` FROM `request_equipment_machine` JOIN  `equipment_machine` ON`request_equipment_machine`.`eq_ma_id`=`equipment_machine`.`ea_ma_id` JOIN `user` ON `request_equipment_machine`.`uid`=`user`.`ulid`"
    res = db.select(qry)
    return render_template('ao/view_equipment_requests.html', data=res)


@app.route('/ao_update_equipment_request/<id>')
def ao_update_equipment_request(id):
    # request_id
    res = {"id": id}
    return render_template('ao/update_equipment_requests.html', data=res)


@app.route('/ao_update_equipment_requests_post', methods=['POST'])
def ao_update_equipment_requests_post():
    from datetime import datetime
    id = request.form['id']
    status = request.form['status']
    db = Db()
    date = datetime.now().strftime("%Y-%m-%d")
    qry = f"UPDATE `request_equipment_machine` SET `status`='{status}',`update_date`='{date}' WHERE `request_id`='{id}'"
    db.update(qry)
    return ao_view_equipment_requests()


# Android

@app.route('/and_register', methods=['POST'])
def and_register():
    name = request.form['name']
    gender = request.form['gender']
    dob = request.form['dob']
    phone = request.form['pn']
    email = request.form['email']
    house_name = request.form['hname']
    place = request.form['place']
    city = request.form['city']
    district = request.form['district']
    state = request.form['state']
    pincode = request.form['pin']
    photo = request.files['photo']
    from datetime import datetime
    file = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
    photo.save(static_path + "\\agriofficer\\" + file)
    fname = "/static/agriofficer/" + file
    password = request.form['password']
    db = Db()
    qry = "INSERT INTO login VALUES('','" + email + "','" + str(password) + "','user')"
    res = db.insert(qry)
    qry1 = "INSERT INTO user VALUES ('','" + str(
        res) + "','" + name + "', '" + gender + "', '" + dob + "', '" + email + "', '" + phone + "', '" + house_name + "', '" + place + "', '" + city + "', '" + district + "', '" + state + "', '" + pincode + "', '" + fname + "')"
    res1 = db.insert(qry1)
    return jsonify(status="ok")


@app.route('/and_login', methods=['POST'])
def and_login():
    username = request.form['username']
    password = request.form['password']
    qry = f"select * from login where uname='{username}' and password='{password}'"
    db = Db()
    res = db.selectOne(qry)
    if res is None:

        return jsonify(status="no")
    else:
        return jsonify(status="ok", lid=res['loginid'])


@app.route('/and_view_profile', methods=['POST'])
def and_view_profile():
    db = Db()
    lid = request.form['lid']
    qry = f"SELECT * FROM `user` WHERE `ulid`='{lid}'"
    res = db.selectOne(qry)
    return jsonify(status="ok", data=res)


@app.route('/and_update_profile', methods=['POST'])
def and_update_profile():
    ulid = request.form['lid']
    name = request.form['name']
    gender = request.form['gender']
    dob = request.form['dob']
    phone = request.form['pn']
    email = request.form['email']
    house_name = request.form['hname']
    place = request.form['place']
    city = request.form['city']
    district = request.form['district']
    state = request.form['state']
    pincode = request.form['pin']
    photo = request.files['photo']
    from datetime import datetime
    file = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
    photo.save(static_path + "\\user\\" + file)
    fname = "/static/user/" + file
    db = Db()
    qry = f"UPDATE `user` SET `name`='{name}',`gender`='{gender}',`dob`='{dob}',`place`='{place}',`city`='{city}',`district`='{district}',`state`='{state}',`pincode`='{pincode}',`email`='{email}',`phone`='{phone}',`photo`='{photo}' WHERE `ulid`='{ulid}'"
    db.update(qry)
    return jsonify(status="ok")


@app.route('/and_insert_chat', methods=['POST'])
def and_insert_chat():
    from datetime import datetime
    from_id = request.form['from_id']
    to_id = request.form['to_id']
    message = request.form['message']
    date = datetime.now().strftime("%Y-%m-%d")
    time = datetime.now().strftime("%H:%M:%S")
    return jsonify(status="ok")


@app.route('/and_view_chat', methods=['POST'])
def and_view_chat():
    return jsonify(status="ok")


@app.route('/and_view_crop', methods=['POST'])
def and_view_crop():
    return jsonify(status="ok")


@app.route('/and_view_ferti_pesti_info', methods=['POST'])
def and_view_ferti_pesti_info():
    db.Db()
    qry = "SELECT * FROM `ferti_pesticide`"
    res = db.select(qry)
    return jsonify(status="ok", data=res)


@app.route('/and_view_govt_policy', methods=['POST'])
def and_view_govt_policy():
    db = Db()
    qry = "SELECT * FROM `group_policy`"
    res = db.select(qry)
    return jsonify(status="ok", data=res)


@app.route('/and_view_notification', methods=['POST'])
def and_view_notification():
    db = Db()
    qry = "SELECT * FROM `notification`"
    res = db.select(qry)
    return jsonify(status="ok", data=res)


@app.route('/and_view_other_farmer_stories', methods=['POST'])
def and_view_other_farmer_stories():
    db = Db()
    qry = "SELECT * FROM `success_stories`"
    res = db.select(qry)
    return jsonify(status="ok", data=res)


@app.route('/and_view_available_eq_and_ma', methods=['POST'])
def and_view_available_eq_and_ma():
    db = Db()
    qry = "SELECT equipment_machine.*,equipment_machine_stock.* FROM `equipment_machine` JOIN `equipment_machine_stock` ON equipment_machine.ea_ma_id=equipment_machine_stock.eq_ma_id"
    res = db.select(qry)
    return jsonify(status="ok", data=res)


@app.route('/and_send_eq_ma_request', methods=['POST'])
def and_send_eq_ma_request():
    from datetime import datetime
    eq_ma_id = request.form['eq_ma_id']
    uid = request.form['lid']
    date = datetime.now().strftime("%Y-%m-%d")
    status = "Pending"
    db = Db()
    qry = f"INSERT INTO `request_equipment_machine`(`eq_ma_id`,`uid`,`request_date`,`status`) VALUES ('{eq_ma_id}','{uid}','{date}','{status}')"
    db.insert(qry)
    return jsonify(status="ok")


@app.route('/and_send_complaints', methods=['POST'])
def and_send_complaints():
    from datetime import datetime
    lid = request.form['lid']
    date = datetime.now().strftime("%Y-%m-%d")
    complaint = request.form['complaint']
    status = "Pending"
    qry = f"INSERT INTO `complaint` (`lid`,`complaint`,`date`,`status`) VALUES ('{lid}','{complaint}','{date}','{status}')"
    db = Db()
    db.insert(qry)
    return jsonify(status="ok")


@app.route('/and_view_reply', methods=['POST'])
def and_view_reply():
    return jsonify(status="ok")


@app.route('/and_add_product', methods=['POST'])
def and_add_product():
    name = request.form['product_name']
    lid = request.form['farmer_lid']
    photo = request.files['photo']
    price = request.form['price']
    return jsonify(status="ok")


@app.route('/and_edit_product', methods=['POST'])
def and_edit_product():
    return jsonify(status="ok")


@app.route('/and_delete_product', methods=['POST'])
def and_delete_product():
    return jsonify(status="ok")


@app.route('/and_view_product', methods=['POST'])
def and_view_product():
    return jsonify(status="ok")


@app.route('/and_view_others_product', methods=['POST'])
def and_view_others_product():
    return jsonify(status="ok")


@app.route('/and_purchase_product', methods=['POST'])
def and_purchase_product():
    return jsonify(status="ok")


@app.route('/and_view_purchase_req', methods=['POST'])
def and_view_purchase_req():
    return jsonify(status="ok")


@app.route('/and_update_purchase_req', methods=['POST'])
def and_update_purchase_req():
    return jsonify(status="ok")


@app.route('/and_view_purchase_history', methods=['POST'])
def and_view_purchase_history():
    return jsonify(status="ok")


@app.route('/and_bank_loans', methods=['POST'])
def and_bank_loans():
    return jsonify(status="ok")


@app.route('/and_view_subsidy', methods=['POST'])
def and_view_subsidy():
    return jsonify(status="ok")


# ❗❗ FLASK RUN ❗❗

if __name__ == '__main__':
    app.run()
