from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>AI Resume Analyzer</title>
    <style>
        * { box-sizing: border-box; }

        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #f1f5fb;
            color: #25334a;
        }

        header {
            background: #173b70;
            color: white;
            padding: 28px 15px;
            text-align: center;
        }

        header h1 { margin: 0 0 10px; }

        nav {
            background: #102d55;
            padding: 14px;
            text-align: center;
        }

        nav a {
            color: white;
            text-decoration: none;
            margin: 0 12px;
        }

        main {
            max-width: 760px;
            margin: 30px auto;
            padding: 20px;
        }

        .card {
            background: white;
            padding: 25px;
            margin-bottom: 22px;
            border-radius: 12px;
            box-shadow: 0 4px 15px #00000012;
        }

        input, textarea {
            width: 100%;
            padding: 12px;
            margin: 8px 0 16px;
            border: 1px solid #ccd5e2;
            border-radius: 6px;
            font-size: 15px;
        }

        textarea { min-height: 110px; }

        button {
            background: #1769d2;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 12px 20px;
            cursor: pointer;
            font-size: 15px;
        }

        button:hover { background: #104d9e; }

        .result {
            background: #eaf4ff;
            padding: 18px;
            border-radius: 8px;
        }

        .job {
            background: white;
            padding: 12px;
            margin: 8px 0;
            border-radius: 6px;
        }

        .error { color: #b42318; }

        footer {
            text-align: center;
            padding: 20px;
            color: #667085;
        }
    </style>
</head>
<body>

<header>
    <h1>AI Resume Analyzer</h1>
    <p>Analyze your skills and explore career opportunities</p>
</header>

<nav>
    <a href="/">Home</a>
    <a href="#analyze">Analyze Resume</a>
    <a href="#jobs">Job Recommendations</a>
    <a href="#about">About</a>
</nav>

<main>
    <section class="card">
        <h2>Welcome!</h2>
        <p>Discover job opportunities based on the skills in your resume.</p>
        <p>This beginner project demonstrates resume skill analysis.</p>
    </section>

    <section class="card" id="analyze">
        <h2>Resume Skills Analyzer</h2>
        <form method="POST">
            <label for="name">Your Name</label>
            <input id="name" name="name" required
                   placeholder="Enter your name"
                   value="{{ name }}">

            <label for="email">Email Address</label>
            <input id="email" name="email" type="email" required
                   placeholder="you@example.com"
                   value="{{ email }}">

            <label for="skills">Skills (separated by commas)</label>
            <textarea id="skills" name="skills" required
                placeholder="Python, SQL, AWS, JavaScript">{{ skills }}</textarea>

            <button type="submit">Analyze My Skills</button>
        </form>
    </section>

    {% if error %}
    <section class="card error">
        <p>{{ error }}</p>
    </section>
    {% endif %}

    {% if result is not none %}
    <section class="card result">
        <h2>Analysis Results</h2>
        <p>Hello, <strong>{{ name }}</strong>!</p>
        <p>Skills entered: <strong>{{ skill_count }}</strong></p>
        <p>Demo score: <strong>{{ result }}/100</strong></p>

        <h3>Skills Identified</h3>
        <p>{{ skill_list | join(", ") }}</p>

        <h3 id="jobs">Recommended Jobs</h3>
        {% for job in jobs %}
        <div class="job">{{ job }}</div>
        {% endfor %}

        <p><small>
        The score is a simple demonstration, not a validated AI assessment.
        Recommendations are based on predefined skill rules.
        </small></p>
    </section>
    {% endif %}

    <section class="card" id="about">
        <h2>About This Project</h2>
        <p>Project: AI-Based Resume Analyzer and Job Recommendation System</p>
        <p>Technology: Python Flask, HTML, CSS and JavaScript-ready web UI.</p>
        <p>Purpose: Demonstrate skill analysis and job recommendation.</p>
    </section>
</main>

<footer>
    Software Testing Project | Resume Analyzer
</footer>

</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():
    name = ""
    email = ""
    skills = ""
    result = None
    jobs = []
    skill_list = []
    error = None

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        skills = request.form.get("skills", "").strip()

        if not name or not email or not skills:
            error = "Please fill in all fields."
        else:
            skill_list = sorted({
                skill.strip().lower()
                for skill in skills.split(",")
                if skill.strip()
            })

            if not skill_list:
                error = "Please enter at least one skill."
            else:
                skill_count = len(skill_list)
                result = min(100, skill_count * 20)

                if any(s in skill_list for s in ["python", "sql", "pandas", "numpy"]):
                    jobs.append("Data Analyst")

                if any(s in skill_list for s in ["java", "javascript", "html", "css"]):
                    jobs.append("Software Developer")

                if any(s in skill_list for s in ["aws", "azure", "gcp", "spark"]):
                    jobs.append("Cloud / Data Engineer")

                if not jobs:
                    jobs.append("Entry-Level IT Trainee")

                return render_template_string(
                    HTML,
                    name=name,
                    email=email,
                    skills=skills,
                    result=result,
                    jobs=jobs,
                    skill_count=skill_count,
                    skill_list=skill_list,
                    error=None
                )

    return render_template_string(
        HTML,
        name=name,
        email=email,
        skills=skills,
        result=result,
        jobs=jobs,
        skill_count=0,
        skill_list=skill_list,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)