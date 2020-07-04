# DESIGN

Project's aim is to create from scratch a code editor for web.
Code editor will include the window for writing code and will allow
execution of code in different programming languages.

## Pipeline

1. The user selects what programming language he chooses to use.
2. The user writes the code in the editor window.
3. The user presses "Run" button.
4. The code is sent via POST request to Flask application.
5. Flask application processes the request and determines what language is used.
6. The app sets 10 sec timeout and passes the application for running in 
   one of the Docker containers.
7. The output is redirected to a file, it is being then read and send as a response to 
   front-end.
8. Front-end receives response and pushes it to the output window.

## Front-end



## Back-end



### Code execution in Docker containers

- Java
- Python
- JavaScript

## Deployment with Docker to Clouds

# Current TODO

- [x] Implement code editor (indentation, syntax highlight, paren matching, identifier search)
- [x] Use docker to create environments for code execution
- [x] Add ability to execute Java, JS, C++, Go
- [ ] Think and read about security and protection against DDOS
- [ ] Think about performance and concurrency
- [x] Implement streaming output directly to browser, not prog->file->json->browser
- [ ] Design and build API system
- [ ] Think whether Python is the right language for this?