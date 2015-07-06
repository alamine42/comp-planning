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

    this_week_master_dict = pull_disqus()
    print "THIS IS THE DICT BEFORE TUMBLR"
    print this_week_master_dict

    for thread in this_week_master_dict.values():
        print "THREAD"
        print thread

        tumblr_post_id = thread['tumblr_post_id']
        tumblr_post = pull_tumblr(tumblr_post_id)
        tumblr_post_short = tumblr_post['posts'][0]
        thread['tumblr_post_body'] = tumblr_post_short['body']
        thread['tumblr_post_timestamp'] = tumblr_post_short['timestamp']
        thread['tumblr_post_title'] = tumblr_post_short['title']
        thread['tumblr_post_date'] = tumblr_post_short['date']

    return this_week_master_dict

# Using decorators, link the application to a url

@app.route("/")
@app.route("/main")
def view_week():

    this_week_dict = create_master()
    print this_week_dict

    ordered_posts = collections.OrderedDict(sorted(this_week_dict.items()))
    return render_template('disqus.html', threads = ordered_posts )

@app.route("/disqus")
def get_disqus_threads():

    threads_dict = pull_disqus()
    
    return render_template('disqus.html', threads = threads_dict)


# Start the development server using the run() method:
if __name__ == "__main__":
    app.run(debug=True)
