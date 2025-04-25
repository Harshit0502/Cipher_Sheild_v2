from flask import Flask, jsonify
from flask_cors import CORS
from routes.auth import auth  # Import the auth blueprint
from routes.message import message_api
from routes.upload import upload_api
from routes.token import token_api
from middleware.logging_middleware import register_logging
from flask_jwt_extended import JWTManager
from utils.sanitizer import sanitize_input
from middleware.rate_limiter import limiter, init_limiter
from redis import Redis
from routes.logs import logs_bp  
from routes.ml_threats import ml_threat_api

def create_app():
    # Initialize the Flask app
    app = Flask(__name__)

    # Enable CORS for all routes and origins
    CORS(app, origins="http://localhost:3000", supports_credentials=True)

    # Set JWT secret key
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this to a strong secret key
    register_logging(app)
    jwt = JWTManager(app)

    init_limiter(app)


    # Register the auth blueprint with url_prefix='/auth'
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(message_api, url_prefix='/chat')
    app.register_blueprint(upload_api, url_prefix='/file')
    app.register_blueprint(token_api, url_prefix='/auth')
    app.register_blueprint(logs_bp)
    app.register_blueprint(ml_threat_api)

    # Add a basic root (/) route for browser test
    @app.route('/')
    def home():
        return jsonify({"msg": "Welcome to the API!"}), 200

    return app

if __name__ == '__main__':
    import os
    print("🚀 Starting Flask App...")

    # Ensure logs directory exists
    if not os.path.exists('logs'):
        os.makedirs('logs')

    app = create_app()
    print("✅ Server running at:")
    print("   → http://127.0.0.1:8000")
    print("   → http://localhost:8000")
    
    app.run(debug=True, port=8000, host='0.0.0.0')
