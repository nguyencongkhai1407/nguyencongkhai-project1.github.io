from django.shortcuts import render
from markdown2 import Markdown
from . import util
import re
from random import randint, seed
from django.http import HttpResponseRedirect

def index(request):
    if request.method == "GET":
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })
    else:
        dl = request.POST
        if util.get_entry(dl['q']) != None:
            render(request, "encyclopedia/title.html", {
                "title":  Markdown().convert(util.get_entry(dl['q'])),
                "name": dl['q']
            })
            return HttpResponseRedirect(f"/wiki/{dl['q']}")
        else:
            pattern = "^" + dl['q'].lower()
            ls = []
            entries = util.list_entries()
            for entry in entries:
                if re.match(pattern, entry.lower()):
                    ls.append(entry)


            return render(request, "encyclopedia/search.html",{
                "name": dl['q'],
                "entries": ls
            })


def getTitle(request, title):
    markdowner = Markdown()
    if util.get_entry(title) != None:
        return render(request, "encyclopedia/title.html", {
            "title":  markdowner.convert(util.get_entry(title)),
            "name": title
        })
    else:
        return render(request,"encyclopedia/error.html",{
            "name": title
        })


def new(request):
    if request.method =="POST":
        data = request.POST
        found = False
        entries = util.list_entries()
        for entry in entries:
            if entry.lower() == data['title'].lower():
                found = True
        if data['markdown'].strip() == "" or found:
            return render(request, "encyclopedia/error2.html")
        else:
            util.save_entry(data["title"], data["markdown"])
            render(request,"encyclopedia/title.html",{
                "name": str(data['title']),
                "title": Markdown().convert(data['title'])
            })
            return HttpResponseRedirect(f"/wiki/{str(data['title'])}")
    else:
        return render(request, "encyclopedia/new.html")



def edit(request,title):
    if request.method =="GET":
        return render(request, "encyclopedia/edit.html",{
            "title": title,
            "markdown":util.get_entry(title)
        })
    else:
        data= request.POST
        util.save_entry(title, data['mark'])
        render(request,"encyclopedia/title.html",{
                "name": title,
                "title": Markdown().convert(util.get_entry(title))
            })
        return HttpResponseRedirect(f"/wiki/{title}")
    

def random(request):
    l= util.list_entries()
    seed(None)
    n = randint(0, len(l)-1)
    title = l[n]
    render(request,"encyclopedia/title.html",{
                "name": title,
                "title": Markdown().convert(util.get_entry(title))
            })
    return HttpResponseRedirect(f"/wiki/{title}")        

       

