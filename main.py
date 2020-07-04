import docker
import config
import tarfile
import os

from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

app = Flask(__name__)

client = docker.from_env()

containers = {
    "python": client.containers.get("python-container"),
    "java": client.containers.get("java-container"),
    "javascript": client.containers.get("node-container")
}

extensions = {
    "python": "py",
    "java": "java",
    "javascript": "js"
}


def get_file_name(lang):
    return config.MAIN_FILE + "." + extensions[lang]


def copy_to(src, dst, container):
    os.chdir(os.path.dirname(src))
    srcname = os.path.basename(src)
    tar = tarfile.open(src + '.tar', mode='w')
    try:
        tar.add(srcname)
    finally:
        tar.close()

    data = open(src + '.tar', 'rb').read()
    container.put_archive(os.path.dirname(dst), data)


def write(text, file_name):
    with open(file_name, 'w') as f:
        f.write(text)


def read(file_name):
    with open(file_name, 'r') as f:
        return f.read()


def pass_to_container(container, code, file_name):
    write(code, file_name)
    copy_to("./" + file_name, "/app/" + file_name, container)
    os.remove(file_name)


def run_code(lang, code):
    file_name = get_file_name(lang)
    container = containers[lang]
    pass_to_container(container, code, file_name)
    output = b""
    if lang == "python":
        _, output = container.exec_run("python {0}".format(file_name))
    elif lang == "java":
        container.exec_run("javac {0}".format(file_name))
        _, output = container.exec_run("java {0}".format(os.path.splitext(file_name)[0]))
    elif lang == "javascript":
        _, output = container.exec_run("node {0}".format(file_name))
    else:
        return b"Language not supported"
    return output


@app.route('/')
def editor():
    return render_template("home.html")


@app.route('/run', methods=['POST'])
def run():
    lang = request.json.get('lang')
    code = request.json.get('code')
    output = run_code(lang, code)
    result = {"output": output.decode()}
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
