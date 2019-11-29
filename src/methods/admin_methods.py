import requests
from flask import request, jsonify
from flask_jwt_simple import JWTManager, create_jwt, get_jwt
from sqlalchemy import desc
from utils import APIException, check_params, validation_link, update_table, sha256, role_jwt_required
from models import db, Users, Profiles, Tournaments, Swaps, Flights, Buy_ins, Transactions, Tokens
from datetime import datetime
from populate_database import run_seeds

def attach(app):


    @app.route('/populate_database')
    @role_jwt_required(['admin'])
    def populate():
        run_seeds()
        return 'Seeds ran!'




    @app.route('/create/token', methods=['POST'])
    def create_token():
        return jsonify( create_jwt(request.get_json()) ), 200




    @app.route('/tournaments', methods=['POST'])
    def add_tournament():
        body = request.get_json()
        db.session.add(Tournaments(
            name = body['name'],
            address = body['address'],
            start_at = datetime( *body['start_at'] ),
            end_at = datetime( *body['end_at'] ),
            longitude = None,
            latitude = None
        ))
        db.session.commit()
        search = {
            'name': body['name'],
            'start_at': datetime( *body['start_at'] )
        }
        return jsonify(Tournaments.query.filter_by(**search).first().serialize()), 200




    @app.route('/flights/<id>')
    def get_flights(id):
        if id == 'all':
            return jsonify([x.serialize() for x in Flights.query.all()])




    @app.route('/flights', methods=['POST'])
    def create_flight():
        body = request.get_json()
        db.session.add(Flights(
            tournament_id = body['tournament_id'],
            start_at = datetime( *body['start_at'] ),
            end_at = datetime( *body['end_at'] ),
            day = body['day']
        ))
        db.session.commit()
        search = {
            'tournament_id': body['tournament_id'],
            'start_at': datetime(*body['start_at']),
            'end_at': datetime(*body['end_at']),
            'day': body['day']
        }
        return jsonify(Flights.query.filter_by(**search).first().serialize()), 200




    @app.route('/buy_ins/<id>')
    def get_buyins(id):
        if id == 'all':
            return jsonify([x.serialize() for x in Buy_ins.query.all()])
        return jsonify(Buy_ins.query.get(int(id)).serialize())




    @app.route('/flights/<id>', methods=['DELETE'])
    def delete_flight(id):
        db.session.delete( Flights.query.get(id) )
        db.session.commit()
        return jsonify({'message':'hoe hoe hoe'}), 200




    @app.route('/tournaments/<id>', methods=['DELETE'])
    def delete_tournament(id):
        db.session.delete( Tournaments.query.get(id) )
        db.session.commit()
        return jsonify({'message':'Tournament deleted by jolly o Saint Nick'}), 200




    @app.route('/buy_ins/<id>', methods=['DELETE'])
    def delete_buy_in(id):
        db.session.delete( Buy_ins.query.get(id) )
        db.session.commit()
        return jsonify({'message':'Buy in deleted, and Santa will put you in the naughty list if you contine deleting stuff'}), 200




    @app.route('/swaps', methods=['DELETE'])
    def delete_swap():
        body = request.get_json()
        db.session.delete( Swaps.query.get(body['sender_id'], body['recipient_id'], body['tournament_id']) )
        db.session.commit()
        return jsonify({'message':"Swap deleted from Santa's list"}), 200



    return app