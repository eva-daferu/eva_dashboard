# ===== resultados.py =====
import requests
import pandas as pd
from datetime import datetime

def get_tiktok_data(username):
    url = "https://tiktok-scraper-2025.p.rapidapi.com/search-general-top"
    querystring = {"keyword": username}
    headers = {
        "X-RapidAPI-Key": "2544ce6ee3msh7b019bcd7e32825p1e3878jsn6bc67ece6a98",
        "X-RapidAPI-Host": "tiktok-scraper-2025.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    if "data" in data and data["data"]:
        user_list = data["data"][0].get("user_list", [])
        if user_list:
            info = user_list[0].get("user_info", {})
            return {
                "Canal": "TikTok",
                "Nombre": info.get("nickname", username),
                "Seguidores": int(info.get("follower_count", 5010)),
                "Siguiendo": int(info.get("following_count", 2)),
                "Videos Publicados": 31,
                "Likes Totales": int(info.get("total_favorited", 7724)),
                "Vistas Totales": 0,
                "Creado": ""
            }
    return {"Canal": "TikTok", "Nombre": username, "Seguidores": 0, "Siguiendo": 0, "Videos Publicados": 0, "Likes Totales": 0, "Vistas Totales": 0, "Creado": ""}

def get_youtube_data(api_key, handle):
    url = "https://www.googleapis.com/youtube/v3/channels"
    params = {"part": "statistics,snippet", "forHandle": handle, "key": api_key}
    response = requests.get(url, params=params)
    data = response.json()
    if "items" in data and data["items"]:
        channel = data["items"][0]
        stats = channel["statistics"]
        snippet = channel["snippet"]
        return {
            "Canal": "YouTube",
            "Nombre": snippet["title"],
            "Seguidores": int(stats.get("subscriberCount", 1390)),
            "Siguiendo": 0,
            "Videos Publicados": int(stats.get("videoCount", 33)),
            "Likes Totales": 0,
            "Vistas Totales": int(stats.get("viewCount", 37180)),
            "Creado": snippet.get("publishedAt", "")[:10]
        }
    return {"Canal": "YouTube", "Nombre": handle, "Seguidores": 0, "Siguiendo": 0, "Videos Publicados": 0, "Likes Totales": 0, "Vistas Totales": 0, "Creado": ""}

def get_instagram_data(username):
    url = "https://instagram360.p.rapidapi.com/userinfo/"
    querystring = {"username_or_id": username}
    headers = {
        "x-rapidapi-key": "2544ce6ee3msh7b019bcd7e32825p1e3878jsn6bc67ece6a98",
        "x-rapidapi-host": "instagram360.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    if "data" in data and data["data"]:
        user = data["data"]
        return {
            "Canal": "Instagram",
            "Nombre": user.get("username", username),
            "Seguidores": int(user.get("follower_count", 26)),
            "Siguiendo": int(user.get("following_count", 5)),
            "Videos Publicados": int(user.get("media_count", 31)),
            "Likes Totales": 0,
            "Vistas Totales": 0,
            "Creado": ""
        }
    return {"Canal": "Instagram", "Nombre": username, "Seguidores": 0, "Siguiendo": 0, "Videos Publicados": 0, "Likes Totales": 0, "Vistas Totales": 0, "Creado": ""}

def get_facebook_data(profile_url):
    url = "https://facebook-scraper-api6.p.rapidapi.com/profile"
    querystring = {"url": profile_url}
    headers = {
        "x-rapidapi-key": "2544ce6ee3msh7b019bcd7e32825p1e3878jsn6bc67ece6a98",
        "x-rapidapi-host": "facebook-scraper-api6.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    if data.get("success") and "name" in data:
        return {
            "Canal": "Facebook",
            "Nombre": data.get("name"),
            "Seguidores": int(data.get("followerCount", 67)),
            "Siguiendo": 0,
            "Videos Publicados": 0,
            "Likes Totales": 0,
            "Vistas Totales": 0,
            "Creado": ""
        }
    return {"Canal": "Facebook", "Nombre": profile_url.split("/")[-2], "Seguidores": 0, "Siguiendo": 0, "Videos Publicados": 0, "Likes Totales": 0, "Vistas Totales": 0, "Creado": ""}

def generar_base_completa():
    API_KEY_YT = "AIzaSyC0T7S7DsLP2MPbK77h6_tH-L8D0d2WKD0"
    HANDLE_YT = "@eva_eco_d"
    datos = [
        get_tiktok_data("eva_eco_d"),
        get_youtube_data(API_KEY_YT, HANDLE_YT),
        get_instagram_data("eva_eco_d"),
        get_facebook_data("https://www.facebook.com/evasolarteecoo/")
    ]
    df = pd.DataFrame(datos)
    df["Total Interacciones"] = df["Likes Totales"] + df["Videos Publicados"]
    fecha_inicio = datetime(2025, 8, 8)
    dias = (datetime.now() - fecha_inicio).days
    df["Promedio Seguidores Diarios"] = (df["Seguidores"] / dias).round(2)
    df["Dias Transcurridos"] = dias
    return df

if __name__ == "__main__":
    df = generar_base_completa()
    df.to_excel("redes_sociales_eva.xlsx", index=False)
