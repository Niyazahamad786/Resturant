from flask import Flask,flash,render_template,url_for,session,request,redirect
from all import app,bcrypt
from all.forms import RegistrationForm,LoginForm,Reserve
import sqlite3
import  datetime 
from datetime import *
conn =sqlite3.connect('data.db',check_same_thread=False)
c=conn.cursor()

c.execute(
    """CREATE TABLE IF NOT EXISTS User(
        id INTEGER PRIMARY KEY,
        username TEXT    NOT NULL UNIQUE,
        email TEXT    NOT NULL UNIQUE,
        password TEXT    NOT NULL

    )""")
c.execute(
"""CREATE TABLE IF NOT EXISTS Person(
    id INTEGER PRIMARY KEY,
    title TEXT  NOT NULL ,
    first_name TEXT    NOT NULL ,
    last_name TEXT    NOT NULL ,
    email TEXT    NOT NULL ,
    phone TEXT    NOT NULL,
    user_id INTEGER    NOT NULL ,
    FOREIGN KEY (User_id)   REFERENCES User(id)

)"""
)

c.execute(
"""CREATE TABLE IF NOT EXISTS Resturant(
    id INTEGER PRIMARY KEY,
    city TEXT  NOT NULL ,
    tabl TEXT  NOT NULL ,
    purpose TEXT    NOT NULL ,
    meal TEXT    NOT NULL ,          
    date date    NOT NULL,
    time TEXT    NOT NULL,
    user_id INTEGER    NOT NULL ,
    person_id INTEGER    NOT NULL ,           
    FOREIGN KEY (User_id)   REFERENCES User(id),
    FOREIGN KEY (person_id)   REFERENCES Person(id)

)"""
)
c.execute(
    """CREATE TABLE IF NOT EXISTS Per_Res(
        id INTEGER PRIMARY KEY,
        per_id INTEGER NOT NULL ,
        res_id INTEGER NOT NULL,
        FOREIGN KEY (per_id)   REFERENCES Person(id),
        FOREIGN KEY (res_id)   REFERENCES Resturant(id)

    )
    """
)

@app.route('/')
@app.route('/home')
def home():
    if 'user' in session:
        
        return render_template('home.html')
    else:
        return redirect(url_for('login'))

@app.route('/reserve',methods=['GET','POST'])
def reserve():
    if 'user' in session:
        form=Reserve()
        if request.method=='POST':
            first=form.first.data
            title=form.title.data
            last=form.last.data
            email=form.email.data
            phone=form.phone.data
            city=form.city.data
            table=form.table.data
            purpose=form.purpose.data
            meal=form.meal.data
            date=form.date.data
            time=form.time.data
            user=session['user']
            user_id=conn.execute("SELECT id FROM User where username=  '" + user + "'")
            users=user_id.fetchall()
            user_id=users[0][0]
            
            with conn:
                conn.execute("INSERT INTO Person(title,first_name,last_name,email,phone,user_id) VALUES (:title,:first_name,:last_name ,:email, :phone,:user_id)", {'title':title,'first_name':first , 'last_name': last, "email": email,"phone":phone,"user_id":user_id })
            person_id=conn.execute("SELECT Person.id FROM User,Person where User.id=Person.user_id and first_name=  '" + first + "' and last_name=  '" + last + "'")
            person=person_id.fetchall()
            person_id=person[0][0]       
            with conn:
                conn.execute("INSERT INTO Resturant(city,tabl,purpose,meal,date,time,user_id,person_id) VALUES (:city,:tabl ,:purpose, :meal,:date,:time,:user_id,:person_id)", {'city':city , 'tabl': table, "purpose": purpose,"meal":meal,"date":date,"time":time,"user_id":user_id,"person_id":person_id })
            rest_id=conn.execute("SELECT Resturant.id FROM Resturant,Person where Resturant.person_id=Person.id and Resturant.city=  '" + city + "' and Resturant.tabl=  '" + table + "' and Resturant.purpose=  '" + purpose + "'  and Resturant.meal=  '" + meal + "' and Resturant.date=  '" + str(date) + "' and Resturant.time=  '" + time + "'and Resturant.user_id=  '" + str(user_id )+ "'")
            re_id=rest_id.fetchall()
            re_id=re_id[0][0]
            with conn:
                conn.execute("INSERT INTO Per_Res(per_id,res_id) VALUES (:per_id,:res_id )", {'per_id':person_id , 'res_id': re_id})
            
            user=session['user']
            iddd=conn.execute("SELECT user.id from user where username='"+user+"'")
            idd=iddd.fetchall()
            idd=idd[0][0]
            perr=conn.execute("SELECT Resturant.user_id,Person.user_id,title,first_name,last_name,tabl,purpose,meal,date,time,Person.id,Resturant.id,Per_Res.id from Person,Resturant,Per_Res where Person.id=Per_Res.per_id and Resturant.id=Per_Res.res_id  ")
            per=perr.fetchall()
            li=[]
            per.reverse() 
            for pe in per:
                if pe[0]==idd and pe[1]==idd:
                    li.append(pe)     
            return render_template('thanks.html')


        return render_template('reserve.html',title='Reserve',form=form)
        
        
    else:
        return redirect(url_for('login'))
    
@app.route('/booking',methods=['GET','POST'])
def booking():
    if 'user' in session:
        user=session['user']
        id=conn.execute("SELECT user.id from user where username='"+user+"'")
        id=id.fetchall()
        id=id[0][0]
        perr=conn.execute("SELECT title,first_name,last_name,tabl,purpose,meal,date,time,Person.id,Resturant.id,Per_Res.id,Resturant.user_id,Person.user_id  from Person,Resturant,Per_Res where Person.id=Per_Res.per_id and Resturant.id=Per_Res.res_id  ")
        per=perr.fetchall() 
        per.reverse()
        li=[]
         
        for pe in per:
            if pe[11]==id and pe[12]==id:
                li.append(pe)
        return render_template('booking.html',per=li)
    else:
        return redirect(url_for('login'))

@app.route('/delete_values/<person_id>/<resturant_id>',methods=['POST'])
def delete_values(person_id,resturant_id):
    if 'user' in session:
        with conn:
            conn.execute("DELETE FROM Person where id='"+str(person_id)+"'")
            conn.execute("DELETE FROM Resturant where id='"+str(resturant_id)+"'")
        return redirect(url_for('booking'))



@app.route('/register',methods=['GET','POST'])
def register():
    if "user" in session:
        return redirect(url_for('home'))  
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_pw=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user1=form.username.data
        em=form.email.data
        em=str(em)
        x=conn.execute("SELECT username,email FROM User ")
        res=x.fetchall()
        users=[]
        emails=[]
        for user in res:
            users.append(user[0])
            emails.append(user[1])
        if user1 in users:
            flash(f'Account already there for {form.username.data}! ','danger')
            return render_template('register.html',title='Regster',form=form)

        elif em in emails:
            flash(f'Account already there for {form.email.data}! ','danger')
            return render_template('register.html',title='Regster',form=form)

        else:

            with conn:
                conn.execute("INSERT INTO User(username,email,password) VALUES (:user, :email, :pass)", {'user':user1 , 'email': em, "pass": hashed_pw })
                flash(f'Account created for {form.username.data}! ','success')
                return redirect(url_for('login'))


    return render_template('register.html',title='Regster',form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        y=conn.execute("SELECT email,password FROM User ")
        result=y.fetchall()
        email=form.email.data
        pass_word=form.password.data
        emails=[]
        passes=[]
        for x in result:
            emails.append(x[0])
            passes.append(x[1])
        login_flag = False 
        for i in range(len(emails)):
            if email==emails[i] and bcrypt.check_password_hash(passes[i],pass_word):
                us_eer=conn.execute("SELECT username FROM User where email=  '" + emails[i] + "'")
                user = us_eer.fetchall()
                session["user"]= user[0][0]
                login_flag = True
                return redirect(url_for('home'))
        if login_flag == False and 'user' not in session:  
            flash('Login Unsuccessful.Please check again' ,'danger')
            return render_template('login.html',title='login',form=form)
    return render_template('login.html',title='login',form=form)


@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop("user",None)
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))
