# Josh Talks Intern Assignment Submission - Backend Task

The query chosen for searching youtube is `cricket`.

## Instructions for running the server

### Install dependencies:
```sh
pip install -r requirements.txt
```

### Set environment variable for Youtube api key:

For Unix/POSIX (Mac and Linux) systems:
```sh
export YOUTUBE_API_KEY=<YOUR_API_KEY>
```

For Windows:
```bat
set YOUTUBE_API_KEY=<YOUR_API_KEY>
```

### Run the server:

```sh
flask run
```

The server should now be running on port 5000.

## Testing the server

The server has two methods:
1. `/search`:
	- `query`: The query string to search for videos.
2. `/videos`:
	- `page`: The page number to return. By default returns 5 videos per page.

**Example URLS**:
 - `http://127.0.0.1:5000/videos?page=1`
 - `http://127.0.0.1:5000/search?query=pakistan`