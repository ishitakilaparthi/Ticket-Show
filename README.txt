run these commands to activate the virtual environment
	cd Ticket-Show
	cd myenv
	cd Scripts\activate
	cd ..

make sure that your system has python and sqlite3 installed

run these commands on the command line to install the required extensions:
	pip install flask
	pip install flask-sqlalchemy
	pip install flask-login
	pip install flask-wtf

run this to start the development server:
	python main.py