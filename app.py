from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)

# A list to store submitted news stories
news_stories = []

# Define a secret key for admin access
ADMIN_SECRET_KEY = 'your_secret_key'

@app.route('/')
def index():
    # Filter only approved stories
    approved_stories = [story for story in news_stories if story['status'] == 'approved']
    return render_template('index.html', news_stories=approved_stories)

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        url = request.form['url']
        status = request.form['status']  # Added line

        # Create a dictionary to represent the news story
        story = {'title': title, 'description': description, 'url': url, 'status': 'pending', 'flag': status}

        # Add the story to the list
        news_stories.append(story)

        return redirect(url_for('index'))

    return render_template('submit.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    # Check if the provided key matches the admin secret key
    if request.method == 'POST':
        provided_key = request.form.get('key')
        if provided_key == ADMIN_SECRET_KEY:
            # Display all stories for admin approval
            return render_template('admin.html', news_stories=news_stories)
        else:
            abort(403)  # Access forbidden if the key is incorrect

    return render_template('admin_login.html')

@app.route('/approve/<int:story_id>')
def approve(story_id):
    # Approve a story by changing its status to 'approved'
    if 0 <= story_id < len(news_stories):
        news_stories[story_id]['status'] = 'approved'

    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)

