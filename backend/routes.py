from app import app,db
from flask import request, jsonify
from models import Friend

# Get all friends
@app.route('/friends', methods=['GET'])
def get_friends():
    friends = Friend.query.all()
    friends = [friend.to_json() for friend in friends]
    return jsonify(friends)

#create a friend
@app.route('/api/friends', methods=['POST'])
def create_friend():
    try :
        data = request.get_json()

        required_fields = ['name', 'role', 'description','gender']
        for field in required_fields:
            if field not in data:
                return jsonify({"msg": f"Missing : '{field}' is required"}), 400   

        name = data.get('name')
        role = data.get('role')
        description = data.get('description')
        gender = data.get('gender')

        # Fetch avatar image based on gender
        if gender == "male":
            img_url = f"https://avatar.iran.liara.run/public/boy?username={name}"
        elif gender == 'female':
            img_url = f"https://avatar.iran.liara.run/public/girl?username={name}"
        else :
            img_url = None

        new_friend = Friend(name=name, role=role, description=description,gender = gender, img_url=img_url)

        db.session.add(new_friend)

        db.session.commit()

        return jsonify(new_friend.to_json()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Failed to create friend!"}), 500
                            
    
#Delete friend
@app.route('/api/friends/<int:id>', methods=['DELETE'])
def delete_friend(id):
    try : 
        friend = Friend.query.get(id)
        if friend is None:
            return jsonify({"error": "Friend not found!"}), 404

        db.session.delete(friend)
        db.session.commit()

        return jsonify({"msg": "Friend deleted successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to delete friend!"}), 500
    
#Update friend
@app.route('/api/friends/<int:id>', methods=['PATCH'])
def update_friend(id):
    try:
        friend = Friend.query.get(id)
        if friend is None:
            return jsonify({"error": "Friend not found!"}), 404

        data = request.get_json()

        friend.name = data.get('name', friend.name)
        friend.role = data.get('role', friend.role)
        friend.description = data.get('description', friend.description)
        friend.gender = data.get('gender',friend.gender)

        db.session.commit()
        return jsonify(friend.to_json()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to update friend!"}), 500