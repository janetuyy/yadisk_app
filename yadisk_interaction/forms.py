from django import forms


class PublicKeyForm(forms.Form):
    """
    форма перехода к ресурсу по публичной ссылке
    """

    public_key = forms.URLField(
        label="",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter public key'})
    )


class AnotherForm(forms.Form):
    """
    форма выхода из удаленного ресурса к форме ввода публичной ссылки
    """

    reset = forms.CharField(widget=forms.HiddenInput(), required=False)
