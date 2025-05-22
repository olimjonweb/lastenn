#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

class UserManager(BaseUserManager):
    def create_user(self, telegram_id, full_name, username=None, phone_number=None, role='customer', password=None):
        if not telegram_id:
            raise ValueError("Telegram ID required")
        user = self.model(
            telegram_id=telegram_id,
            full_name=full_name,
            username=username,
            phone_number=phone_number,
            role=role
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('driver', 'Driver'),
        ('logistic', 'Logistic'),
        ('customer', 'Customer'),
    )

    telegram_id = models.BigIntegerField(unique=True)
    full_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'telegram_id'
    REQUIRED_FIELDS = ['full_name']
