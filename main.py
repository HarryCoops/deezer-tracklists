import http.server
import requests
import re
import webbrowser
import urllib.parse

from starlette.applications import Starlette
from starlette.responses import JSONResponse, Response
from starlette.routing import Route


async def homepage(request):
    return JSONResponse({'hello': 'world'})


async def auth(request):
    print(request.query_params["code"])
    return Response("OK")

app = Starlette(debug=True, routes=[
    Route('/', homepage),
    Route('/authfinish', auth),
])
