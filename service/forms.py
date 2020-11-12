from django import forms


class PermissionForm(forms.Form):
    perm = forms.BooleanField()
