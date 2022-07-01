import xmlrpc.client
from flask import Flask, request
import xmlrpc.client

import ssl
from waitress import serve



try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

app = Flask(__name__)


# Logs in to Odoo server
# Move to ENV variables



url = "http://localhost:8069"
db = "demo_"
username = "user@email.com"
password = "secure_password"

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})


## Route for testing if app/server is up 


@app.route("/test", methods=['POST', 'GET'])
def hello():
    return "<h1 style='color:blue'>Connector Web Server Is Up! See logs If Trouble Shooting</h1>"
    



## The main route for the app


@app.route('/listener', methods=['POST'])
def listener():
    if request.method == 'POST':

        # Catches the post Webhooks/JSON from source and goes in, gets the product/sku/qty and the customer.

        content = request.json
    
        
        
        #JSON configuration for the product/QTYs customers 
        
        ## Depending on source the set up will be different.
        ## The below is just an example of how to set up the JSON for the source.

        invnm = content[0]['InvoiceNumber']
        noi = (len(content[0]['OrderItemList']))
        orderstatus = content[0]['OrderStatusID']
        internalcomments = content[0]['InternalComments']
        customer_email = content[0]['BillingEmail']
        first_name = content[0]['BillingFirstName']
        last_name = content[0]['BillingLastName']
        customer_id = content[0]['CustomerID']
       
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

        customer = models.execute_kw(db, uid, password,
                                     'res.partner', 'search',
                                     [[['id', '=', customer_id]]])
        print(customer)

        if not customer:
            print("Customer not in odoo")

            # Handle creating a new customer in Odoo

        else:
            print("customer already exists")
            
            print('do things')
            print(orderstatus)
            if orderstatus == 10:
                ## handling for special order status
    
        
        
                    print('special order status')
                    customer_look_up = models.execute_kw(db, uid, password,
                                                         'res.partner', 'search_read',
                                                         [[['id', '=', customer_id]]])

        


                    # Swap product SKUs for product IDs in Odoo. Not ideal, but works for now.
                    # Moving to different utility function

                    swaps_for_products = []

                 
                    
                  
                    
                    
                    changetos = {'23423322322': 10,
                                '232323123332': 1,
                                '232132323233': 4,
                                '231232132332': 5,}


                    for d in content:
                        for i in d["OrderItemList"]:
                            swaps_for_products.append(i.get("ItemID"))
                            swaps_for_products.append(i.get("ItemQuantity"))

                    product_id_swaps = [changetos.get(x, x) for x in swaps_for_products]

        
                    ### Sales lines for sale.order, the number of these are based on the number of items in the order.NOI
        
        
        
                    sales = (0, 0, {'product_id': '', 'product_uom_qty': ''}),
                    #Change b to a more accurate variable name
                    b = [(0, 0, {'product_id': '', 'product_uom_qty': ''}) for _ in range(noi)]

                    start_index = 0
                    b = list(b)
                    for b_entry in b:
                        end_endex = start_index + len(b_entry[2]) - 1
                        for value in range(start_index, end_endex):
                            b_entry[2]['product_id'] = product_id_swaps[value]
                            b_entry[2]['product_uom_qty'] = product_id_swaps[value + 1]
                        start_index += len(b_entry[2])

                    # Handle special product algorithms. IE if certain product break down further into multiple products.

                    def repair_item(item):
                        if item["product_id"] == 1222 and item["product_uom_qty"] >= 45:
                            origina_quantity = item["product_uom_qty"]
                            item["product_id"] = 2222
                            item["product_uom_qty"] //= 45
                            new_q = item["product_uom_qty"]
                            print(origina_quantity)
                            print(new_q)
                            b.append((0, 0, {'product_id': 13, 'product_uom_qty': origina_quantity - 45 * new_q}))

                        else:
                            pass

                    for _, _, item in b:
                        repair_item(item)

        

       
                    b = tuple(b)
                    print(b)
                    
                    
                    
                    
                    ## Check if order already exists in Odoo. Odoo does not allow the same name for sale.order records.
                    
                    new_order = models.execute_kw(db, uid, password,
                                                  'sale.order', 'search',
                                                  [[['name', '=', 'Sales' + str(invnm)]]],
                                                  {'limit': 1}
                                                  )


                    if not new_order:

                      

                        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
                        so_id = models.execute_kw(db, uid, password, 'sale.order', 'create', [{
                            'name': 'Sales:' + str(invnm),
                            'partner_id': customer[0],
                            'state': 'sale',
                            'client_order_ref': 'Retail',
                            'order_line': b

                        }])
                       

                        notes = models.execute_kw(db, uid, password, 'mail.message', 'create', [{
                            'model': 'sale.order',
                            'res_id': so_id,  # from/reference channel
                            'body': internalcomments  # here add the message body

                        }])

                    else:
                        
                        
                        ## Handle order updates. IE if the order had a change in products, the order will be updated.

                        print('order already exist, begin update')
                   
                    return 'success',200
            
                    
                    

        
            else:
                
                return "Order Status is not special", 400





         
            



        




if __name__ == '__main__':
    # app.run(host='0.0.0.0')
    serve(app, host='localhost', port=5000, url_scheme='http')





