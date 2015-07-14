from flask import Flask, render_template, request, session, flash, redirect, url_for
from pytumblr import TumblrRestClient

import json, collections, requests

# Create application object
app = Flask(__name__)

app.config.from_object(__name__)

def pull_disqus():
    result = requests.get('https://disqus.com/api/3.0/forums/listThreads.json?forum=cfsacompetitors&api_key=HniEaWj7WrLq5litkDwbHALAduc405zJ0SSgPQhScXYjC0Dx2ImHWz2AXecY7BH3&limit=7')
    result_dict = json.loads(result.text)
    
    filtered_dict = {}

    for thread in result_dict['response']:

        filtered_dict[thread['id']] = {
            'link': thread['link'],
            'posts': thread['posts'],
            'date' : thread['createdAt'],
            'tumblr_post_id': str(thread['link'])[-12:]
        }

    return filtered_dict

def pull_disqus_comments(thread_id):

    query_string = 'https://disqus.com/api/3.0/threads/listPosts.json?thread=' + thread_id + '&api_key=HniEaWj7WrLq5litkDwbHALAduc405zJ0SSgPQhScXYjC0Dx2ImHWz2AXecY7BH3'

    comments_results = requests.get(query_string)
    comments_results_dict = json.loads(comments_results.text)

    filtered_comments_dict = {}

    for comment in comments_results_dict['response']:

        filtered_comments_dict[ comment['id'] ] = {
            'author': comment['author']['name'],
            'message': comment['message'],
            'raw_message': comment['raw_message']
        }

    return filtered_comments_dict

def pull_tumblr(post_id):

    client = TumblrRestClient(
        'q3K5ba44O1DLAv39TDsp4fEMNY1pGAdXsiciIQQqZdAsXF54Zt',
        'UnkAeG6I7PRHidVqikB3zcrL6DI94q0woJv5sIeUCj3B7ndCdJ',
        'KT75Gar86W3elQAuU7VyiT9UUstfX6JAFGTvG01pJYKStqlAXN',
        'ZggEOt83VSC2lzvN01SWmFJy98r13oeuWyciXxfxVqOwAvo81n'
    )

    # print client.info()

    tumblr_post = client.posts('cfsacompetition.tumblr.com', type='text', id=post_id)

    return tumblr_post

def create_master():

    # Fetch the threads for the past 7 days
    this_week_master_dict = pull_disqus()
    # print "THIS IS THE DICT BEFORE TUMBLR"
    # print this_week_master_dict

    # For each thread, just take the parameters you want
    for thread_key, thread in this_week_master_dict.items():
        # print "THREAD"
        # print thread

        tumblr_post_id = thread['tumblr_post_id']
        tumblr_post = pull_tumblr(tumblr_post_id)
        tumblr_post_short = tumblr_post['posts'][0]
        thread['tumblr_post_body'] = tumblr_post_short['body']
        thread['tumblr_post_timestamp'] = tumblr_post_short['timestamp']
        thread['tumblr_post_title'] = tumblr_post_short['title']
        thread['tumblr_post_date'] = tumblr_post_short['date']

        # Pull the comments for this thread
        thread['comments'] = pull_disqus_comments(thread_key)

    return this_week_master_dict

# Using decorators, link the application to a url

@app.route("/")
@app.route("/main")
def view_week():

    this_week_dict = create_master()
    # print this_week_dict

    ordered_posts = collections.OrderedDict(sorted(this_week_dict.items()))
    return render_template('index.html', threads = ordered_posts )

@app.route("/disqus")
def get_disqus_threads():

    threads_dict = pull_disqus()
    
    return render_template('disqus.html', threads = threads_dict)


# Start the development server using the run() method:
if __name__ == "__main__":
    app.run(debug=True)
