var input = CodeMirror.fromTextArea(document.getElementById("input"), {
    lineNumbers: true,
    mode: "python",
    styleActiveLine: true,
    matchBrackets: true
});

input.setSize("100%", "100%");

var output = CodeMirror.fromTextArea(document.getElementById("output"), {
    lineNumbers: true,
    mode: "string",
    readOnly: true
});

var langs = {
    "python": "",
    "java": "class Main {\n  public static void main(String[] args) {\n    System.out.println(\"Java hello world!\");\n  }\n}",
    "javascript": "console.log('JS hello world!');"
};

$("#lang-select").on('focus', function() {
    langs[this.value] = input.getValue();
}).change(function() {
    input.setOption("mode", this.value == "java" ? "text/x-java" : this.value);
    input.getDoc().setValue(langs[this.value]);
});

function writeOut(text) {
    output.getDoc().setValue(text["output"]);
}

function process() {
    let value = input.getValue();
    let lang = $("#lang-select").val()
    console.log(value);
    console.log(lang)
    $.ajax({
        type: "POST",
        url: "/run",
        data: JSON.stringify({"code": value, "lang": lang }),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: writeOut,
        failure: writeOut,
        error: writeOut
    });
};

