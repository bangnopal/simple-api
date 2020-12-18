from flask import *
from urllib.parse import *
from requests import get, post
from bs4 import BeautifulSoup as bs
from lib.nulis import tulis
import os, random, re, html_text

# Inisiasi
app = Flask(__name__)


# Membuat route/response handler

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
 return {
  "code": "200",
  "status": "sukses",
  "result": "Halo guys, selamat datang di simple API"
 }

# Nulis di buku
@app.route('/nulis', methods=['GET', 'POST'])
@app.route('/tulis', methods=['GET', 'POST'])
def nulis():
    if request.args.get('text'):
        try:
            nulis = tulis(request.args.get('text'))
            for i in nulis:
                i.save('img/tulis.jpg')
            return {
                "code": "200",
                "status": "sukses",
                "result": "tulis.jpg"
            }
        except Exception as e:
            print(e)
            return {
                "code": "500",
                "status": "error",
                "message": "Terjadi masalah pada sisi server, silahkan coba lagi dalam beberapa menit!"
            }
    else:
        return {
            "code": "404",
            "status": "error",
            "message": "Masukan parameter text"
        }

# Youtube Downloader
@app.route('/dl/ytdl', methods=['GET', 'POST'])
def ytdl():
 if request.args.get('url'):
  result = get('https://turu-api.herokuapp.com/dl/ytdl?apikey=demo&url=' + request.args.get('url')).json()
  if result['code'] != "200":
   return {
    "code": "404",
    "status": "error",
    "message": "URL yang anda berikan tidak valid"
   }
  else:
   return {
    "code": "200",
    "status": "sukses",
    "thumbnail": result['thumbnail'],
    "duration": result['duration'],
    "title": result['title'],
    "url": result['url_video'],
    "description": result['description']
   }
 else:
  return {
   "code": "404",
   "status": "error",
   "message": "Masukan parameter url"
  }

# Info gempa
@app.route('/infogempa', methods=['GET', 'POST'])
def gempa():
    try:
        bmkg = bs(get('https://www.bmkg.go.id/').text, 'html.parser').find('div', class_="col-md-4 md-margin-bottom-10")
        scrape = bmkg.findAll('li')
        maps = bmkg.find('a')['href']

        return {
            "code": "200",
            "status": "sukses",
            "result": {
                "maps": maps,
                "waktu": scrape[0].text,
                "magnitude": scrape[1].text,
                "kedalaman": scrape[2].text,
                "koordinat": scrape[3].text,
                "lokasi": scrape[4].text,
                "potensi": scrape[5].text
            },
            "sumber": "https://www.bmkg.go.id/"
        }
    except Exception as e:
        return {
            "code": "404",
            "status": "error",
            "message": "tidak ada data untuk ditampilkan"
        }

# Chord lagu
@app.route('/chord', methods=['GET', 'POST'])
def chord():
    if request.args.get('query'):
        try:
            query = request.args.get('query').replace(' ', '+')
            search = get('http://app.chordindonesia.com/?json=get_search_results&exclude=date,modified,attachments,comment_count,comment_status,thumbnail,thumbnail_images,author,excerpt,content,categories,tags,comments,custom_fields&search=%s' % query).json()['posts'][0]['id']
            chord = get('http://app.chordindonesia.com/?json=get_post&id=%s' % search).json()
            result = html_text.parse_html(chord['post']['content']).text_content()

            return {
                "code": "200",
                "status": "sukses",
                "result": result
            }
        except:
            return {
                "code": "404",
                "status": "error",
                "message": "Chord yang anda minta tidak dapat ditemukan"
            }
    else:
        return {
            "code": "404",
            "status": "error",
            "message": "Masukan parameter query"
        }

# random loli
@app.route('/randomloli', methods=['GET', 'POST'])
def randomloli():
 try:
  kocok = ['kawaii', 'neko']
  randomloli = get('https://api.lolis.life/%s' %random.choice(kocok)).json()
  return {
   "code": "200",
   "status": "sukses",
   "result": randomloli['url']
  }
 except:
  return {
   "code": "503",
   "status": "error",
   "message": "Terjadi masalah pada sisi server, silahkan coba lagi dalam beberapa menit"
  }


# Showing a static images from img/tulis.jpg
@app.route('/img/nulis.jpg', methods=['GET', 'POST'])
@app.route('/img/tulis.jpg', methods=['GET', 'POST'])
def show_tulis():
    return send_file('./img/tulis.jpg')


# Handling 500 error
@app.errorhandler(500)
def error500(e):
    return {
        "code": "500",
        "status": "error",
        "message": "Terjadi masalah pada sisi server, silahkan coba lagi dalam beberapa menit!"
    }

# Handling 404 error
@app.errorhandler(404)
def error404(e):
 return {
  "code": "404",
  "status": "error",
  "message": "endpoint yang kamu tuju tidak dapat ditemukan!"
 }



if __name__ == "__main__":
 # Jika debug=True maka response json akan terlihat lebih rapih, sebaliknya jika False/tidak diisi maka akan mengembalikan response json yg kurang rapih
 app.run(debug=True, host='0.0.0.0')