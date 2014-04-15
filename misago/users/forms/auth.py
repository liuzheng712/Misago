from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.forms import (AuthenticationForm as
                                       BaseAuthenticationForm)
from django.utils.translation import ugettext_lazy as _
from misago.core import forms


class AuthenticationForm(forms.Form, BaseAuthenticationForm):
    """
    Base class for authenticating users, Floppy-forms and
    Misago login field comliant
    """
    username = forms.CharField(label=_("Username or e-mail"), max_length=254)
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    error_messages = {
        'invalid_login': _("Your login or password is incorrect. Please try again."),
        'inactive': _("This account is inactive."),
    }

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)
            if self.user_cache is None:
                raise ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class AdminAuthenticationForm(AuthenticationForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        self.error_messages.update({
            'not_staff': _("Your account does not have admin privileges.")
            })

    def confirm_login_allowed(self, user):
        if not user.is_staff:
            raise forms.ValidationError(
                self.error_messages['not_staff'],
                code='not_staff',
            )