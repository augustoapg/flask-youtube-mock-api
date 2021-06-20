from flask import Flask, request
from flask_restful import Api, Resource, abort, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)


class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name = {self.name}, views = {self.views}, likes = {self.likes})"


if not database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
    db.create_all()
else:
    print("DB already exists")

video_put_args = reqparse.RequestParser()
video_put_args.add_argument(
    "name", type=str, help="Name of video is required", required=True
)
video_put_args.add_argument(
    "views", type=int, help="Views of video is required", required=True
)
video_put_args.add_argument(
    "likes", type=int, help="Likes on video is required", required=True
)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str)
video_update_args.add_argument("views", type=int)
video_update_args.add_argument("likes", type=int)

resource_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "views": fields.Integer,
    "likes": fields.Integer,
}


class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()

        if not result:
            abort(404, message=f"Video {video_id} not found")

        return result

    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()

        if result:
            abort(409, message=f"Video with id {video_id} already exists")

        video = VideoModel(
            id=video_id, name=args["name"], views=args["views"], likes=args["likes"]
        )
        db.session.add(video)
        db.session.commit()
        return video, 201

    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        video = VideoModel.query.filter_by(id=video_id).first()

        if not video:
            abort(404, message=f"Video {video_id} not found")

        print(args)

        if args["name"]:
            video.name = args["name"]
        if args["views"]:
            video.views = args["views"]
        if args["likes"]:
            video.likes = args["likes"]

        db.session.commit()

        return video, 200

    def delete(self, video_id):
        video = VideoModel.query.filter_by(id=video_id).first()

        if not video:
            abort(404, message=f"Video {video_id} not found")

        db.session.delete(video)
        db.session.commit()
        return "Video deleted successfully", 200


class All_Videos(Resource):
    @marshal_with(resource_fields)
    def get(self):
        result = VideoModel.query.order_by(VideoModel.id).all()
        return result


api.add_resource(Video, "/video/<int:video_id>")
api.add_resource(All_Videos, "/video")

if __name__ == "__main__":
    app.run(debug=True)
