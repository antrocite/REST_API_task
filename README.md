Hello!

--------Run the backend server side:------------
On Linux or Mac:

1. Go to 'backend/' directory in terminal
2. $ source venv/bin/activate
   (venv)$ python app.py
3. ???
4. You should see flask server running on http://127.0.0.1:5001/ 

You cant test it with POSTMAN:
    [GET] '/curr' to get all currencies available in DataBase
    [GET] '/curr/<curr_name> to get specific currency with name <curr_name>
    [POST] '/curr/<curr_name> to post new currency with <curr_name>. 
        Header : Content-type application/JSON. 
        Body: {
            "buy_rate" : 75,
            "sell_rate" : 85
        }
    [PUT] '/curr/<curr_name> is same as POST but will update the info if it is already present.
    [DELETE] '/curr/<curr_name> to delete specific currency named <curr_name>

On Windows:

1. Go to 'backend/' directory in terminal
2. $ ./venv/Scripts/activate.bat
   $ python app.py
I'm sorry if it doesn't work. I have only tested on Linux


--------Run frontend client side--------------

1. Go to frontend/ directory in terminal
2. $ npm install 
    OR 
2. $ yarn install (probably)
3. npm audit fix (as for me, maybe you don't need it)
4. npm run serve
5. ???
6. You should see Vue server running on http://localhost:8080/

!!! P.S :

    This project was my very first time working in any front-end JS frameworks.

I've tried to figure it all out on my own but it obviously takes some more than few days,
so, I made frontend following this guide: https://testdriven.io/blog/developing-a-single-page-app-with-flask-and-vuejs/#flask-setup

Thus, I do not claim to have done UI part by my own. Backend is completely mine though.
Nevertheless, I am really looking forward in learning it, I already started one great online course on that.

Also, frontend has one unsolved problem - delete button is not clickable.
I really couldn't figure that one out(At the moment), but I will solve it later.


