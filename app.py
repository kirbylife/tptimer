# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from flask import render_template
from flask import make_response
from flask import session
from flask import redirect
from flask import url_for
from flask import flash

from flask_wtf import CSRFProtect

from config import DevelopmentConfig

from models import db
from models import User
from models import Time

import forms

from pyTwistyScrambler import scrambler222,scrambler333,scrambler444,scrambler555,scrambler666,scrambler777,skewbScrambler,squareOneScrambler,clockScrambler,pyraminxScrambler,megaminxScrambler

def main(args):
    server=Flask(__name__)
    server.config.from_object(DevelopmentConfig)
    csrf=CSRFProtect()

    @server.route("/404")
    @server.errorhandler(404)
    def error404(error=""):
        if ("username" in session):
            return render_template("404.html", username=session["username"]),404
        else:
            return render_template("404.html"),404

    @server.before_request
    def beforeRequest():
        if("id" in session and request.endpoint in ["login","signup"]):
            return redirect(url_for("index"))

    @server.route('/')
    def index():
        if("username" in session):
            return render_template("stopwatch.html",userrname=session["username"])
        else:
            return render_template("stopwatch.html")

    @server.route('/login', methods=["GET","POST"])
    def login():
        login_form = forms.LoginForm(request.form)
        if request.method == "POST" and login_form.validate():
            username = login_form.username.data
            password = login_form.password.data

            user = User.query.filter_by(username=username).first()
            if user is not None and user.verifyPassword(password):
                session["id"]=user.id
                session["username"]=user.username
                return redirect(url_for("index"))
            else:
                flash(u"Usuario o contraseña invalida")
        return render_template('login.html', form = login_form)

    @server.route('/signup', methods=["GET", "POST"])
    def signup():
        signup_form = forms.SignupForm(request.form)
        if(request.method == "POST" and signup_form.validate()):
            wcaId=None
            if(signup_form.wcaId.data!=""):
                wcaId=signup_form.wcaId.data[1:]
            user = User(
                    signup_form.username.data,
                    wcaId,
                    signup_form.email.data,
                    signup_form.password.data,
                )
            db.session.add(user)
            db.session.commit()
            flash("Usuario registrado exitosamente")
            return redirect(url_for("login"))
        return render_template('signup.html', form=signup_form)

    @server.route('/logout')
    def logout():
        if("id" in session):
            session.pop("id")
            session.pop("username")
        return redirect(url_for("index"))

    @server.route('/users/<user>')
    def users(user):
        username=None
        if ("username" in session):
            username=session["username"]
        user=User.query.filter_by(username=user).first()
        if(user==None):
            return redirect(url_for("error404"))
        time2=Time.query.filter_by(user=user.id,cube="2x2x2").all()
        time3=Time.query.filter_by(user=user.id,cube="3x3x3").all()
        time4=Time.query.filter_by(user=user.id,cube="4x4x4").all()
        time5=Time.query.filter_by(user=user.id,cube="5x5x5").all()
        time6=Time.query.filter_by(user=user.id,cube="6x6x6").all()
        time7=Time.query.filter_by(user=user.id,cube="7x7x7").all()
        timesqr=Time.query.filter_by(user=user.id,cube="squareone").all()
        timeskw=Time.query.filter_by(user=user.id,cube="skewb").all()
        timemega=Time.query.filter_by(user=user.id,cube="megaminx").all()
        time3pira=Time.query.filter_by(user=user.id,cube="piraminx").all()
        return render_template("users.html",user=user.username,username=username,t2=time2,t3=time3,t4=time4,t5=time5,t6=time6,t7=time7,tsqr=timesqr,tskw=timeskw,tmega=timemega,tpira=time3pira)

    @server.route("/records")
    def records():
        if("username" in session):
            return render_template("records.html",username=session["username"])
        else:
            return render_template("records.html")

    @server.route("/galeria")
    def galeria():
        if ("username" in session):
            return render_template("galeria.html", username=session["username"])
        else:
            return render_template("galeria.html")

    @server.route("/setTime")
    def setTime():
        if("username" in session):
            cube=request.args.get("cube")
            time=request.args.get("time")
            displayTime=request.args.get("displayTime")
            scramble=request.args.get("scramble")
            newTime=Time(session["id"],cube,time,displayTime,scramble)
            db.session.add(newTime)
            db.session.commit()
            return "Tiempo grabado con exito"
        else:
            return "Primero inicia sesion y luego vemos"


    @server.route('/generateScramble/<cube>',methods=["GET","POST"])
    def generateScramble(cube):
        if(cube == "2x2x2"):
            return scrambler222.get_WCA_scramble()
        elif(cube == "3x3x3"):
            return scrambler333.get_WCA_scramble()
        elif(cube == "4x4x4"):
            return scrambler444.get_WCA_scramble()
        elif(cube == "5x5x5"):
            return scrambler555.get_WCA_scramble()
        elif(cube == "6x6x6"):
            return scrambler555.get_WCA_scramble()
        elif(cube == "7x7x7"):
            return scrambler555.get_WCA_scramble()
        elif(cube == "piraminx"):
            return pyraminxScrambler.get_WCA_scramble()
        elif(cube == "clock"):
            return clockScrambler.get_WCA_scramble()
        elif(cube == "megaminx"):
            return megaminxScrambler.get_WCA_scramble()
        elif(cube == "squareone"):
            return squareOneScrambler.get_WCA_scramble()
        elif (cube == "skewb"):
            return skewbScrambler.get_WCA_scramble()

    csrf.init_app(server)
    db.init_app(server)

    with server.app_context():
        db.create_all()

    server.run()

if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv))
