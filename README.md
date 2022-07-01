# Odoo Sales Connect

A Flask app that lets you connect JSON data, and make sales orders in Odoo. 

## Installation

Tested in Odoo 10-15. 

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install -r requirements.txt
```

## Set Up

A one-time JSON input config will need to be made, so the app knows how to handle the JSON data. Under the line #60 I've shown some examples. IE: If you get webhooks from WOO or pull from an API. 
If you need help with this open an issue or feel free to email me fabiananguiano@ gmail [.]com


Once the JSON app is set up, you can run it over NGINX. 



### User

Once the route http://localhost:5000/listener gets hit with a POST request the JSON will be taken and broken down into Odoo input data. A sale.order record will be created in Odoo. 

You can customize the records to your needs/wants. 


## Todos
* Move to Django 4
* Make a generic unknown customer handler
* Add docker
* Make more examples for JSON data. 
