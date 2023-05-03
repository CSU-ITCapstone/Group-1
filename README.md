# Group-1
**About the Project:**

This is a simple task managing program that the user can add, delete, filter out tasks. The user can also check how many tasks are there as well as how many tasks are by status and priority. 

**Render Info:**

Link to render(tinyurl): https://tinyurl.com/taskmanagerapp1

Link to render (actual): https://taskmanager-group1.onrender.com

**Python Info:**

This program is running the latest version of python 
To check what the current version of python you are running type this command:
```console
$ python
```
- current version as of 4-27-2023 is 3.8.16

**To get this program running the following packages needs to be installed and the pip version has to be updated. To do this:**

First update pip by typing this command:
```console
$ pip install --upgrade pip     
```
- current version as of 4-10-2023 is 23.0.1

Then Install Flask by typing this command:
```console
$ pip install flask
```
Then install pyMongo by typing this command:
```console
$ pip install flask_pymongo
```
Then run the program by typing:
```console
$ python app.py
```
The program should be running without errors

**Another way to run the program still using the initial libraries is to use gunicorn.** 

This makes use of the file titled *Procfile* .

To install the gunicorn library type this command:
```console
$ pip install gunicorn
```
Once that is installed you can run the program by typing:
```console
$ gunicorn app:app
```
The program should be running without errors