from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request

import album

@route("/albums/<artist>")
def albums(artist):
	albums_list = album.find(artist)
	if not albums_list:
		message = "Альбомов {} не найдено!!!!!!!".format(artist)
		result = HTTPError(404, message)
	else:
		album_names = [album.album for album in albums_list]
		count = len(album_names)
		result = "Всего альбомов {} и список альбомов {}: ".format(count, artist)
		result += ", ".join(album_names)
	return result

@route("/albums", method="POST")
def create_album():
    year = request.forms.get("year")
    artist = request.forms.get("artist")
    genre = request.forms.get("genre")
    album_name = request.forms.get("album")

    try:
        year = int(year)
    except ValueError:
        return HTTPError(400, "Указан некорректный год альбома")

    try:
        new_album = album.save(year, artist, genre, album_name)
    except AssertionError as err:
        result = HTTPError(400, str(err))
    except album.AlreadyExists as err:
        result = HTTPError(409, str(err))
    else:    
        print("New id{} album successfully saved".format(new_album.id))
        result = "Альбом id{} успешно сохранен".format(new_album.id)
    return result


@route("/hello/")
def hello_world():
	return "Hello World!"

@route("/upper/<param>")
def upper(param):
	return param.upper()

def fib(n):
	a, b = 1, 1
	for x in range(n):
		a, b = b, a + b
	return a

@route("/fib/<n:int>")
def fib_handler(n):
	result = fib(n)
	return str(result)
	
@route("/modify/<param>/<method>")
def modify(param, method):
	if method == "upper":
		result = param.upper()
	elif method == "lower":
		result = param.lower()
	elif method == "title":
		result = param.title()
	else:
		result = HTTPError(400, "incorrect 'method' value")
	return result

@route("/add")
def add():
	try:
		x=int(request.query.x)
		y=int(request.query.y)
	except ValueError:
		result = HTTPError(400, "Очень некорректные параметры!!!")
	else:
		s = x + y
		result = "Сумма {} и {} равна {}".format(x, y, s)
	return result

	
if __name__=="__main__":
	run(host="localhost", port=8080, debug=True)
