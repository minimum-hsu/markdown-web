#!/usr/bin/env python3

from markdown import markdown
from flask import Flask, render_template, Markup
from os import listdir
from os.path import dirname, isfile, isdir, join, relpath, abspath
import re

CURRENT_DIR = dirname(abspath(__file__))
MARKDOWN_DIR = join(CURRENT_DIR, 'markdown')

app = Flask(
    __name__,
    static_folder = 'static',
    template_folder = 'templates'
)

@app.errorhandler(FileNotFoundError)
@app.errorhandler(404)
def page_not_found(e):
    return '<h1>Page not found</h1>', 404

def markdown2html(mdfile, title = None):
    content = ''
    with open(mdfile, 'r') as f:
        content = f.read()
    md = markdown(
        content,
        output_format = 'html5',
        tab_length = 2,
        lazy_ol = False,
        extensions = [
            'markdown.extensions.tables'
        ]
    )
    title = title or 'Markdown'
    content = Markup(md)
    return render_template('markdown.html', **locals())

@app.route('/', methods = ['GET'])
def index():
    f = join(MARKDOWN_DIR, 'index.md')
    return markdown2html(f) if isfile(f) \
        else '<h1>Welcome to Markdown World!</h1>'

def build_api(path):
    rule = relpath(path, MARKDOWN_DIR)
    function_name = re.sub(r'\W', '_', rule)
    app.logger.debug('build {}'.format(function_name))

    def func(page):
        mdfile = join(path, '{}.md'.format(page))
        app.logger.debug(mdfile)
        return markdown2html(mdfile)

    func.__name__ = function_name
    rule = '/<page>' if rule == '.' \
        else '/{}/<page>'.format(rule)
    app.add_url_rule(
        rule,
        endpoint = function_name,
        view_func = func,
        methods = ['GET']
    )

def traverse(dir):
    build_api(dir)
    for d in listdir(dir):
        absdir = join(dir, d)
        if isdir(absdir):
            traverse(absdir)

traverse(MARKDOWN_DIR)
