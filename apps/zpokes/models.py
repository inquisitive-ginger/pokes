from __future__ import unicode_literals

from django.db import models

from django.core.validators import MinLengthValidator

import bcrypt

class User(models.Model):
    name = models.CharField(max_length=45)
    alias = models.CharField(max_length=45)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255, validators=[MinLengthValidator(8, 'Password must be at least 8 characters.')])
    date_of_birth = models.DateField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    # password encryption
    def set_password(self, raw_password):
        self.password = bcrypt.hashpw(raw_password.encode(), bcrypt.gensalt())

    # validate password
    def check_password(self, raw_password):
        return self.password == bcrypt.hashpw(raw_password.encode(), self.password.encode())

class Poke(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    poker = models.ForeignKey(User, related_name='poker')
    pokee = models.ForeignKey(User, related_name='pokee')
