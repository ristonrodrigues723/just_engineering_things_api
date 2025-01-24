# Welcome to My RaspAPI YSWS Submission 🚀

This is my entry for the RaspAPI YSWS program—a lighthearted yet practical API crafted for engineers and messy people like me. Honestly, trying to get it live almost drove me mad. 😅

This API provides a fun collection of engineering-themed jokes, facts, and quotes while also letting users contribute their own jokes or rate existing ones. It's fully tested on both PowerShell and Linux terminals, ensuring simplicity, reliability, and a touch of engineering humor!

## Features 🎉

- **GET Jokes**: Fetch all the jokes available in the database.
- **GET Quotes**: Retrieve a list of all quotes. (I even added one by me!)
- **GET Facts**: Explore interesting facts from the database.
- **POST Jokes**: Submit your own jokes to the database.
- **POST Rating**: Rate jokes, quotes, or facts on a scale of 1–5.

I’ve tested this API 40–50 times both locally and on the hosted version, so dive in and give it a try!

## How to Use

### GET Jokes
Fetch a list of all jokes. (Not including my current state!)
```bash
curl -X GET https://maximus723.hackclub.app/jokes
```
**PowerShell Example:**
```powershell
Invoke-RestMethod -Uri https://maximus723.hackclub.app/jokes -Method GET
```

### GET Quotes
Retrieve a list of quotes.
```bash
curl -X GET https://maximus723.hackclub.app/quotes
```
**PowerShell Example:**
```powershell
Invoke-RestMethod -Uri https://maximus723.hackclub.app/quotes -Method GET
```

### GET Facts
Fetch fun facts.
```bash
curl -X GET https://maximus723.hackclub.app/facts
```
**PowerShell Example:**
```powershell
Invoke-RestMethod -Uri https://maximus723.hackclub.app/facts -Method GET
```

### POST Jokes
Submit a new joke.
```bash
curl -X POST https://maximus723.hackclub.app/jokes \
-H "Content-Type: application/json" \
-d '{"content": "Why did the chicken cross the road? To get to the other side!"}'
```
**PowerShell Example:**
```powershell
Invoke-RestMethod -Uri https://maximus723.hackclub.app/jokes -Method POST -Body @{
    content = "Why did the chicken cross the road? To get to the other side!"
}
```

### POST Rating
Rate a joke, quote, or fact. Provide the `content_id` and your rating (1–5).
```bash
curl -X POST https://maximus723.hackclub.app/rate/1 \
-H "Content-Type: application/json" \
-d '{"rating": 5}'
```
**PowerShell Example:**
```powershell
Invoke-RestMethod -Uri https://maximus723.hackclub.app/rate/1 -Method POST -Body @{
    rating = 5
}
```

## Behind the Scenes 🧜‍♂️

This project is something I’m super proud of! Here’s the story:

1. I started following a YouTube video to build a Flask API, but it quickly went wrong. 😬
2. Backtracked,started from scratch reading a blog  made changes as per needs and guidelines blog was about transaction api mine was a joke api, and initially used a list to store jokes, quotes, and facts when testing locally. But I realized the list wasn’t updating on POST requests.
3. Switched to using a `.json` file for storage. Later, I added POST functionality for ratings so users could rate jokes, quotes, and facts.
4. Tried hosting on Railway, but it failed. Debugged like crazy, but no luck.
5. Moved to Vercel, but discovered Vercel can’t store `.json` files as persistent data. After some head-scratching, migrated to Firebase for the database tried vercel again but after 5 hrs of headscratching back to the same point.
6. so i Hosted the API on Hack Club Nest after consulting documentation and Slack channels and helpful people. (Nest is awesome! and the helpers too)

## Challenges Faced 🛠️

- tried using Swagger for documentationit didn’t work—it kept getting messed up tried using ai for help to debug still same to did a simple webage as documentation.
- Debugging issues with `.env` variables on Vercel and hosting on it was headcracking so hosted on nest .
- hosting flask api on vercela nd railwauy is messy.


Finally, I created this index page with simple instructions for accessing the API.

**Helpful Resources:**
I also followed [this blog](https://auth0.com/blog/developing-restful-apis-with-python-and-flask/) on developing RESTful APIs with Python and Flask. It explains how to create a transaction API, but the advanced steps got messed up for me, so I adapted it for my needs.

---
© 2025 Jokes API | Built with ❤️ by a 16-year-old teen who learned a lot along the way!

