from flask import Flask
import os

def create_app(test_config=None):
    app=Flask('__name__',
                instance_relative_config=True, 
                template_folder='portal/templates',
                static_folder='portal/static')
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'portal.sqlite')
    )
   
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return '<h1>Hello, World!</h1>'

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)

    app.add_url_rule("/", endpoint="auth.index")

    return app