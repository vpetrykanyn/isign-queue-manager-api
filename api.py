from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
import uuid

from rq import Queue
from rq.job import Job
from worker import conn

app = FlaskAPI(__name__)

q = Queue(connection=conn)

# TODO: logging
# assumptions: worker nodes could be on Heroku or AWS
# message bus is required
# authentication is required

@app.route("/api/v1/resign", methods=['POST'])
def resign():
    gitlab_id = str(request.data.get('gitlab_id', ''))
    client_list = str(request.data.get('client_list', ''))

    job = q.enqueue_call(
        func=count_and_save_words, args=(url,), result_ttl=5000
    )
    print(job.get_id())

    return {'gitlab_id': gitlab_id, 'id': uuid.uuid4() }, status.HTTP_201_CREATED

@app.route("/api/v1/poll/<id>", methods=['GET'])
def poll(id):
    # look up job in the queue
    # statuses should be in_progress, uploading_results, done, canceled
    return { 'id': id, 'status': 'done' }


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
