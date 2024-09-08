import requests
from django.http import HttpResponse
from django.shortcuts import render
from typing import List, Dict, Any

from yadisk_interaction.forms import PublicKeyForm, AnotherForm


def get_all_files(public_key: str, path: str = "") -> List[Dict[str, Any]]:
    """
    функция получения содержимого удаленного ресурса
    """
    url = f"https://cloud-api.yandex.net/v1/disk/public/resources?public_key={public_key}&path={path}"
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


def download_files(request) -> Dict[str, Any]:
    """
    функция скачивания файлов удаленного ресурса
    """
    if request.method == "POST":
        path = request.POST.get("download")
        public_key = request.POST.get("public_key")
        print(public_key)
        download_url = f"https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={public_key}&path={path}"
        headers = {
            "Authorization": "y0_AgAAAAAWZ9fnAAxg3wAAAAEP4FZdAAAq_KWXPvlJMrOBbr-c0ch6HryEPQ",
        }
        response = requests.get(download_url, headers=headers)
        if response.status_code == 200:
            link = response.json().get("href")
            file_response = requests.get(link, stream=True)
            if file_response.status_code == 200:
                file_name = path.split("/")[-1]  # Извлекаем имя файла из пути
                response = HttpResponse(
                    file_response.content, content_type="application/octet-stream"
                )
                response["Content-Disposition"] = f'attachment; filename="{file_name}"'
                return response
        else:
            return render(
                request,
                "yadisk_interaction/download.html",
                {"error": "Failed to download files"},
            )
    return render(
        request,
        "yadisk_interaction/download.html",
        {"error": "Failed to download files"},
    )


def yandex_disk_view(request):
    """
    функция просмотра с содержимого удаленного ресурса
    """
    if request.method == "POST":
        form = PublicKeyForm(request.POST)
        another_form = AnotherForm(request.POST)
        if form.is_valid():
            public_key = form.cleaned_data["public_key"]
            path = request.POST.get("path", "")
            files_and_folders = get_all_files(public_key, path)
            return render(
                request,
                "yadisk_interaction/index.html",
                {
                    "files_and_folders": files_and_folders,
                    "form": form,
                    "public_key_received": True,
                    "public_key": public_key,
                    "path": path,
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
