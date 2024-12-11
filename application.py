from flask import Flask, jsonify, redirect
from flask_restful import Api, MethodNotAllowed, NotFound
from flask_cors import CORS
from util.common import domain, port, prefix, build_swagger_config_json
from resources.swaggerConfig import SwaggerConfig
from resources.employeeResource import (
    EmployeeGETResource,
    EmployeeEntryGETResource,
    EmployeePOSTResource,
    EmployeePUTResource,
    EmployeeDELETEResource,
)
from flask_swagger_ui import get_swaggerui_blueprint

# ============================================
# Main
# ============================================
application = Flask(__name__)
app = application
app.config['PROPAGATE_EXCEPTIONS'] = True
CORS(app)
api = Api(app, prefix=prefix, catch_all_404s=True)

# ============================================
# Swagger
# ============================================
build_swagger_config_json()
swaggerui_blueprint = get_swaggerui_blueprint(
    prefix,
    f'http://{domain}:{port}{prefix}/swagger-config',
    config={
        'app_name': "Employee Mental Health Prediction API",
        "layout": "BaseLayout",
        "docExpansion": "none"
    },
)
app.register_blueprint(swaggerui_blueprint)

# ============================================
# Error Handler
# ============================================
@app.errorhandler(NotFound)
def handle_method_not_found(e):
    response = jsonify({"message": str(e)})
    response.status_code = 404
    return response

@app.errorhandler(MethodNotAllowed)
def handle_method_not_allowed_error(e):
    response = jsonify({"message": str(e)})
    response.status_code = 405
    return response

@app.route('/')
def redirect_to_prefix():
    if prefix != '':
        return redirect(prefix)

# ============================================
# Add Resource
# ============================================
# Add resources for employee data
api.add_resource(EmployeeGETResource, "/employee")  # Get all employees
api.add_resource(EmployeeEntryGETResource, "/employee/<string:id>")  # Get specific employee by ID
api.add_resource(EmployeePOSTResource, "/employee")
api.add_resource(EmployeePUTResource, "/employee/<string:id>")
api.add_resource(EmployeeDELETEResource, "/employee/<string:id>")
api.add_resource(SwaggerConfig, "/swagger-config")

if __name__ == '__main__':
    app.run(debug=True)
