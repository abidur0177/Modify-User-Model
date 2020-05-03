from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueErro('The email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(('first name'), max_length=150, blank=True)
    last_name = models.CharField(('last name'), max_length=150, blank=True)
    email = models.EmailField(('email address'), blank=True, unique=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(('date joined'), default=timezone.now)
    mobile = models.CharField(("Mobile Number"), blank=True, max_length=20)
    address = models.TextField(("User Address"), blank=True)


    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    objects = UserManager()


    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')


    def __str__(self):
        return self.email

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()








# Create your models here.
'''class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name=("User"), related_name = ("customer"), on_delete=models.CASCADE)
    mobile = models.CharField(("Mobile Number"), max_length=20)
    address = models.TextField(("User Address"))

    def __str__(self):
        return self.user.username'''

'''class User(AbstractUser):
    mobile = models.CharField(("Mobile Number"), max_length=20)
    address = models.TextField(("User Address"))

    def __str__(self):
        return self.username'''
