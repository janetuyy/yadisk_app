import requests
from django.shortcuts import render
from typing import List, Dict, Any

from yadisk_interaction.forms import PublicKeyForm, AnotherForm


def get_all_files(public_key: str) -> List[Dict[str, Any]]:
    """
    функция просмотра содержимого удаленного ресурса
    """
    url = (
        f"https://cloud-api.yandex.net/v1/disk/public/resources?public_key={public_key}"
    )
    headers = {
        "Authorization": "y0_AgAAAAAWZ9fnAAxg3wAAAAEP4FZdAAAq_KWXPvlJMrOBbr-c0ch6HryEPQ",
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        items = data.get("_embedded", {}).get("items", [])
        return items
    else:
        print(f"Error: {response.status_code}")
        print(f"Response: {response.text}")
        return []


def yandex_disk_view(request):
    """
    основная функция взаимодействия с содержимым удаленного ресурса
    """
    if request.method == "POST":
        form = PublicKeyForm(request.POST)
        another_form = AnotherForm(request.POST)
        if form.is_valid():
            public_key = form.cleaned_data["public_key"]
            files_and_folders = get_all_files(public_key)
            return render(
                request,
                "yadisk_interaction/index.html",
                {
                    "files_and_folders": files_and_folders,
                    "form": form,
                    "public_key_received": True,
                },
            )
        elif another_form.is_valid():
            return render(
                request,
                "yadisk_interaction/index.html",
                {
                    "form": PublicKeyForm(),
                    "reset_form": AnotherForm(),
                    "public_key_received": False,
                },
            )
    else:
        form = PublicKeyForm()
        another_form = AnotherForm()

    return render(
        request,
        "yadisk_interaction/index.html",
        {"form": form, "another_form": another_form, "public_key_received": False},
    )
