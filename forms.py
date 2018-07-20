# -*- coding: utf-8 -*-

from wtforms import Form
from wtforms import StringField
from wtforms import PasswordField
from wtforms import validators
from wtforms.fields.html5 import EmailField

import requests
import re

def validateWCAID(form,field):
    regex=r"[\d]{4}[\w]{4}[\d]{2}"
    if(field.data!=""):
        if(field.data[0]!="#"):
            raise validators.ValidationError("Introduce tu WCA-ID con un '#' al principio")
        if(re.match(regex,field.data[1:])==None):
            raise validators.ValidationError("Introduce una WCA-ID valida")
        if(requests.get("https://www.worldcubeassociation.org/persons/"+field.data[1:]).status_code!=200):
            raise validators.validationError("Introduce una WCA-ID valida")


class LoginForm(Form):
    username = StringField(u"Nombre de usuario o #WCA-ID *",
            [
                validators.DataRequired("Ingrese un nombre de usuario o #WCA-ID"),
                validators.length(min=0,max=25,message="Ingrese un nombre de usuario valido")
            ])
    password = PasswordField(u"Contraseña *",
            [
                validators.required(u"Ingrese su contraseña")
            ])

class SignupForm(Form):
    username = StringField(u"Nombre de usuario *",
            [
                validators.DataRequired("Este campo es requerido"),
                validators.length(min=0,max=25,message="Ingrese un nombre de usuario valido")
            ])
    wcaId = StringField(u"#WCA-ID",[
                validateWCAID
            ])
    email = EmailField(u"Correo electronico *",[
                validators.DataRequired("Este campo es requerido"),
                validators.Email("Introduce una direccion de email valida")
            ])
    password = PasswordField(u"Contraseña *",[
                validators.DataRequired("Este campo es requerido")
            ])