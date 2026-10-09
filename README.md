# ✨ Weekend Spark

### Turn your ideas into a blueprint. Find your next step. Start building.

**Weekend Spark** is an AI-powered project-planning agent that transforms project ideas into tailored solutions, practical next steps, and AWS architecture recommendations. It also drafts AWS Builder Center articles to help builders document and share their projects.

🚀 **[Try the Live Demo](https://aws-weekend-challenge-eshq95xptp2nnhbucqy2yh.streamlit.app/)**

<img width="955" height="389" alt="image" src="https://github.com/user-attachments/assets/16452990-6550-4a2d-a785-a65799192eac" />


---

## 📌 About the Project

Have you ever had an exciting project idea but struggled to figure out where to start?

Weekend Spark helps solve that problem. Describe your idea, identify your target audience, and share one detail that would make the project special. Spark turns your input into a structured project blueprint with relevant AWS service recommendations.

Built for students, developers, cloud learners, and weekend makers, Weekend Spark helps make the first step toward building something real a little easier.

## ✨ Features

* **💡 AI-Powered Planning:** Transform project ideas into tailored solutions and practical build plans.
* **🎙️ Voice Input:** Speak your idea using the browser's supported speech-recognition capabilities.
* **✏️ Editable Transcripts:** Review and correct recognized speech before generating a blueprint.
* **☁️ AWS Architecture Recommendations:** Receive service suggestions based on your project's requirements.
* **📝 Builder Center Article Generator:** Draft a project-focused article with architecture explanations and the `#agents` tag.
* **⚡ Local Preview Mode:** Explore the planning workflow without AWS credentials.
* **🤖 Amazon Bedrock Integration:** Generate context-aware blueprints and articles using a configured Amazon Bedrock model.

## 🛠️ Technology Stack

| Technology             | Purpose                    |
| ---------------------- | -------------------------- |
| Python                 | Core application logic     |
| Streamlit              | Interactive web interface  |
| Amazon Bedrock Runtime | Optional AI inference      |
| Boto3                  | AWS SDK for Python         |
| Bedrock Converse API   | Model interaction          |
| Web Speech API         | Browser-based speech input |
| Python `unittest`      | Automated offline checks   |

## 🏗️ Proposed AWS Architecture

The following architecture describes potential future hosting and supporting services. **The prototype does not automatically deploy or provision these AWS resources.**

```text
              User
                |
                v
       Streamlit Web Interface
       (Potentially hosted on
        Amazon ECS + Fargate)
                |
                v
       Python Planning Agent
                |
                v
       Amazon Bedrock Runtime
          (Model Inference)
                |
                v
       Project Blueprint
       + AWS Recommendations
       + Builder Center Article

    Optional Future Components
    --------------------------
    Amazon S3       -> File storage
    Amazon DynamoDB -> Draft persistence
    AWS IAM         -> Access control
    CloudWatch      -> Monitoring
    CloudTrail      -> API activity auditing
```

### How It Works

1. The user enters or speaks a project idea.
2. Spark processes the brief using Local preview or Amazon Bedrock mode.
3. The planner generates a tailored solution and relevant AWS service recommendations.
4. Spark prepares a practical next step and can draft a Builder Center article from the same brief and blueprint.
5. The user reviews the output and decides what to build next.

## 🚀 Getting Started

### Prerequisites

* Python 3.10 or a compatible version supported by the project's dependencies.
* Git (optional, for cloning the repository).
* An AWS account and configured AWS credentials if you want to use Amazon Bedrock mode.

### 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd <YOUR_PROJECT_DIRECTORY>
```

Replace the placeholders with your actual repository URL and directory name.

### 2. Create a Virtual Environment

**Windows PowerShell**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
streamlit run app.py
```

Open the local URL provided by Streamlit in your terminal.

## ⚙️ Using Weekend Spark

### Local Preview

1. Open the application.
2. Select **Local preview**.
3. Enter a project idea or use the voice-input feature.
4. Review and edit the idea as needed.
5. Generate your blueprint and explore the recommendations.

Local preview does not send project content to AWS.

### Amazon Bedrock Mode

1. Select **Amazon Bedrock**.
2. Enter an AWS Region and a model ID or inference-profile ID available to your account.
3. Configure AWS credentials through the standard AWS credential chain.
4. Submit your project brief and generate the desired output.

**Privacy note:** In Bedrock mode, the submitted project brief, including the idea, audience, and delightful detail, is sent to Amazon Bedrock for processing. Browser speech recognition may also use the browser provider's speech service. Review the applicable service policies before submitting sensitive information.

## 🧪 Run the Tests

Run the offline test suite with:

```bash
py -m unittest -v
```

These checks help validate supported application behavior, including recommendations and article generation.

## 📂 Project Structure

```text
Weekend-Spark/
├── app.py
├── agent.py
├── requirements.txt
├── article.md
├── assets/
│   └── weekend-spark-proof.png
├── components/
│   └── speech_input/
└── README.md
```

*Note: This structure reflects the documented project contents. Keep it aligned with the actual files in your repository.*

## 🎯 Project Goals

* Reduce the friction between having an idea and starting a project.
* Make AWS service selection easier to understand.
* Encourage small, achievable development steps.
* Help builders document and share their work.
* Explore practical AI-agent development with Amazon Bedrock.

## 🔮 Future Improvements

* Save and revisit project blueprints.
* Add more rigorous evaluation of AWS architecture recommendations.
* Improve personalization for different builder experience levels.
* Expand agent capabilities and workflow testing.
* Explore secure, scalable AWS hosting and optional persistent storage.

## 📜 Disclaimer

Weekend Spark provides project-planning assistance and AWS service recommendations for educational and prototyping purposes. Recommendations should be reviewed against your application's requirements, security needs, expected workload, and budget before implementation.

The current prototype does not automatically deploy AWS resources. AWS services mentioned in the proposed architecture are not necessarily provisioned or in use.

## 👨‍💻 Built for Builders

Weekend Spark is built around one simple idea: **you don't need the entire roadmap to take the first step.**

Start with an idea. Get a blueprint. Build something meaningful.

