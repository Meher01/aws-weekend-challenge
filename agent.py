from __future__ import annotations


def _suggested_services(problem: str) -> list[tuple[str, str]]:
    """Map idea signals to a small set of plausible AWS building blocks."""
    idea = problem.casefold()
    services: list[tuple[str, str]] = []

    def add(name: str, reason: str) -> None:
        if name not in {service for service, _ in services}:
            services.append((name, reason))

    if any(word in idea for word in ("agent", "assistant", "generative ai", "llm", "chatbot", "chat bot", "ai ")):
        add("Amazon Bedrock", "Generate grounded responses with a foundation model; invoke through Bedrock Runtime Converse.")
        add("Amazon Bedrock AgentCore Runtime", "Host a custom agent loop with managed execution.")
    if any(word in idea for word in ("website", "frontend", "landing page", "portfolio", "static site")):
        add("AWS Amplify Hosting", "Deploy a frontend with managed builds, hosting, and a delivery network.")
    if any(word in idea for word in ("web app", "web application", "streamlit", "python app", "containerized")):
        add("Amazon ECS on AWS Fargate", "Run a containerized web application without managing servers.")
    if any(word in idea for word in ("api", "backend", "serverless", "webhook")):
        add("Amazon API Gateway", "Expose a secure HTTP API for the app or its integrations.")
        add("AWS Lambda", "Run request handlers and business logic without managing servers.")
    if any(word in idea for word in ("relational", "sql", "transactions", "booking", "orders", "inventory", "payments")):
        add("Amazon RDS for PostgreSQL", "Store related records and transactional data in a managed relational database.")
    elif any(word in idea for word in ("database", "user profile", "profiles", "session", "preferences", "history")):
        add("Amazon DynamoDB", "Store application records in a managed key-value and document database.")
    if any(word in idea for word in ("upload", "file", "image", "photo", "document", "video", "audio")):
        add("Amazon S3", "Store uploaded files durably, with access controls and lifecycle policies.")
    if any(word in idea for word in ("sign in", "sign-in", "login", "log in", "authentication", "accounts")):
        add("Amazon Cognito", "Add managed user sign-up, sign-in, and token-based authentication.")
    if any(word in idea for word in ("search", "catalog", "knowledge base", "documents", "rag")):
        add("Amazon Bedrock Knowledge Bases", "Retrieve relevant passages from project content to ground generated answers.")
    if any(word in idea for word in ("email", "notification", "alert", "reminder", "message")):
        add("Amazon SNS", "Deliver event-driven notifications to subscribers or downstream integrations.")
    if any(word in idea for word in ("queue", "background", "async", "asynchronous", "job", "process later")):
        add("Amazon SQS", "Queue work for reliable background processing and retry handling.")
    if any(word in idea for word in ("analytics", "dashboard", "reporting", "metrics", "data pipeline")):
        add("Amazon Athena", "Query files in S3 for analytics without operating a database server.")
    if not services:
        add("AWS Amplify Hosting", "A straightforward way to publish a small web experience and iterate on it.")
        add("Amazon DynamoDB", "An optional managed store if the prototype needs to retain user-created records.")
    return services[:8]


def _recommended_build_path(problem: str, services: list[tuple[str, str]]) -> list[str]:
    steps = [
        f"Build one screen around the core user task: {problem}",
        f"Connect only the first backend capability you need ({services[0][0]}) and test it with sample data.",
    ]
    if len(services) > 1:
        steps.append(f"Add {services[1][0]} only when the first end-to-end flow works.")
    steps.append("Test an empty input and one realistic example; then decide whether hosting, persistence, or sign-in is truly needed.")
    return steps


def _architecture_flow(services: list[tuple[str, str]]) -> str:
    names = {name for name, _ in services}
    flow = ["User"]
    if "Amazon Cognito" in names:
        flow.append("Amazon Cognito (sign-in)")
    if "AWS Amplify Hosting" in names:
        flow.append("AWS Amplify Hosting")
    if "Amazon ECS on AWS Fargate" in names:
        flow.append("Amazon ECS on AWS Fargate")
    if "Amazon API Gateway" in names:
        flow.extend(["Amazon API Gateway", "AWS Lambda"])
    if "Amazon Bedrock AgentCore Runtime" in names:
        flow.append("Amazon Bedrock AgentCore Runtime")
    if "Amazon Bedrock Knowledge Bases" in names:
        flow.append("Amazon Bedrock Knowledge Bases")
    if "Amazon Bedrock" in names:
        flow.append("Amazon Bedrock")
    if "Amazon S3" in names:
        flow.append("Amazon S3 (uploaded files)")
    if "Amazon DynamoDB" in names:
        flow.append("Amazon DynamoDB")
    if "Amazon RDS for PostgreSQL" in names:
        flow.append("Amazon RDS for PostgreSQL")
    if "Amazon SNS" in names:
        flow.append("Amazon SNS")
    if "Amazon SQS" in names:
        flow.append("Amazon SQS")
    return " → ".join(flow)


def _article_word_limit(article: str, limit: int = 800) -> str:
    """Keep generated stories within the challenge's requested maximum."""
    article = article.strip()
    if not article:
        raise ValueError("The article generator returned no content. Please try again.")
    if "#agents" not in article:
        article = f"{article}\n\n#agents"
    words = article.split()
    if len(words) <= limit:
        return article

    shortened = " ".join(words[: limit - 1])
    final_sentence = max(shortened.rfind(". "), shortened.rfind("! "), shortened.rfind("? "))
    if final_sentence > 0:
        shortened = shortened[: final_sentence + 1]
    return f"{shortened.rstrip()} #agents"


def _bedrock_text(prompt: str, region: str, model_id: str, max_tokens: int) -> str:
    if not region or not model_id:
        raise ValueError("Enter an AWS Region and a Bedrock model or inference profile ID.")

    import boto3
    from botocore.config import Config

    client = boto3.client(
        "bedrock-runtime",
        region_name=region,
        config=Config(retries={"max_attempts": 5, "mode": "adaptive"}),
    )
    response = client.converse(
        modelId=model_id,
        messages=[{"role": "user", "content": [{"text": prompt}]}],
        inferenceConfig={"maxTokens": max_tokens, "temperature": 0.65},
    )
    text = "".join(
        block["text"]
        for block in response["output"]["message"]["content"]
        if "text" in block
    ).strip()
    if not text:
        raise ValueError("Amazon Bedrock returned no text. Check the model response and try again.")
    return text


def generate_plan(
    project_name: str,
    audience: str,
    problem: str,
    delightful_detail: str,
    use_bedrock: bool = False,
    region: str = "",
    model_id: str = "",
) -> str:
    """Create a focused weekend plan using Bedrock or the offline preview."""
    if not all(value.strip() for value in (project_name, audience, problem, delightful_detail)):
        raise ValueError("Please complete all four idea fields before asking for a plan.")
    if len(project_name) > 100 or len(audience) > 300 or len(problem) > 1200 or len(delightful_detail) > 300:
        raise ValueError("Keep the project name under 100 characters, audience and delightful detail under 300 each, and idea under 1,200.")

    if use_bedrock:
        prompt = f"""You are Weekend Spark, a warm, practical solution architect. Turn the user's actual idea into a focused blueprint, not a generic weekend plan. Infer the key capabilities from the idea. Suggest only AWS services that directly support those capabilities (usually 2-5), and explain why each service fits. Include a concise possible architecture flow in the order data/request moves through the selected services. Include a deploy option only if it is relevant. Do not list unrelated services. Do not assume anything is deployed. Return clear Markdown with exactly these sections: The promise; Who it helps; The solution; Suggested AWS services (bulleted list with service name and rationale, followed by a possible architecture flow); Build path (4 concrete milestones); Tiny win (a measurable test of the delightful detail). Keep it actionable, friendly, jargon-light, and avoid invented requirements.

Project: {project_name}
Audience: {audience}
Project idea: {problem}
Delightful detail: {delightful_detail}
"""
        return _bedrock_text(prompt, region, model_id, max_tokens=1100)

    services = _suggested_services(problem)
    build_path = _recommended_build_path(problem, services)
    service_list = "\n".join(f"- **{name}** — {reason}" for name, reason in services)
    milestones = "\n".join(f"{index}. {step}" for index, step in enumerate(build_path, start=1))

    flow = _architecture_flow(services)
    return f"""### The promise
**{project_name}** helps {audience} solve this problem: “{problem}”

### Who it helps
Start with one specific builder, not every possible user: **{audience}**. The smallest useful version is a working path through the main task, without optional infrastructure until the core experience proves valuable.

### The solution
Build a focused first version that lets a user complete the central task—**{problem}**—and clearly shows what happened. Begin with sample data and a simple interface; add only the backend capabilities needed to make the main flow real.

### Suggested AWS services
These are options inferred from your project idea, not resources created by Spark:

{service_list}

**Possible architecture flow:** {flow}

### Build path
{milestones}

### Tiny win
Make the first response feel achievable: **{delightful_detail}**. Ask someone to try one realistic example and observe whether they can complete the core task without coaching. Add data storage, sign-in, and production hosting only when the prototype needs them."""


def generate_article(
    brief: dict[str, str],
    plan: str,
    use_bedrock: bool = False,
    region: str = "",
    model_id: str = "",
) -> str:
    """Draft a Builder Center article about the user's project blueprint."""
    if use_bedrock:
        prompt = f"""Write a polished Builder Center article, 550 to 700 words, about the user's project idea—not an article primarily about Weekend Spark. The article is for the AWS agent-building weekend challenge. Output Markdown only, using this structure:
# A specific, engaging title about the user's project
## Project description
Describe what the user plans to create and who it is for, grounded in the brief.
## The problem and the proposed solution
Explain the need and how the proposed project would help.
## Proposed AWS workflow and architecture
Explain the request/data flow in order. Explain each relevant AWS service by its exact name and its role in this project's workflow. Use only services from the supplied blueprint; do not invent additional services. Clearly say these services are proposals, not deployed infrastructure.
## How I would build it
Give a realistic, small first implementation path tied to the proposed flow.
## The experience and how to test it
Include the delightful detail from the brief and a measurable way to test it, without claiming testing has already happened.
## How this blueprint was made
Briefly state that Weekend Spark is a Python/Streamlit agent with local preview and optional Amazon Bedrock via boto3 Converse. This is context, not the main subject.
## Proof it works
Reference assets/weekend-spark-proof.png as proof of the Weekend Spark blueprint interface, not proof that the user's proposed project or AWS architecture is deployed.
Finish with the literal tag #agents.
Keep the complete article between 500 and 800 words including headings and tag. Do not claim deployments, user studies, or outcomes that are not in the brief. Use the project name as the article title. Make the generated architecture and service explanations the main body, not a generic story about Spark. Output the article only.

Brief: {brief}
Generated solution blueprint (the exact proposed service names, rationales, and workflow source): {plan}
"""
        article = _bedrock_text(prompt, region, model_id, max_tokens=1400)
        return _article_word_limit(article)

    project = brief.get("project_name", "Weekend Spark")
    audience = brief.get("audience", "AWS builders with a weekend-sized idea")
    problem = brief.get("problem", "turning a promising idea into a shippable plan")
    project_idea = problem.strip().rstrip(".!?")
    delight = brief.get(
        "delightful_detail",
        "end every plan with one tiny, finishable next step",
    )
    service_lines = [
        line
        for line in plan.splitlines()
        if line.startswith("- **Amazon ") or line.startswith("- **AWS ")
    ]
    tailored_services = "\n".join(service_lines) or "- No AWS service recommendations were found in the blueprint. Keep the first version local until a concrete need is identified."
    flow_line = next(
        (
            line.removeprefix("**Possible architecture flow:**").strip()
            for line in plan.splitlines()
            if line.startswith("**Possible architecture flow:**")
        ),
        "Begin with the user request, then connect only the services listed below when the project needs them.",
    )

    article = f"""# {project}: a practical blueprint for {audience}

## Project description

{project} is a project the builder plans to create for **{audience}**. Its starting idea is: **{project_idea}**. The goal is to turn that need into a small, usable experience with a clear path from a person's request to a helpful result. The first version should focus on this central task, then add supporting capabilities only where the project genuinely needs them.

## The problem and the proposed solution

The project addresses a need described by its builder: {project_idea}. The proposed solution is to give the intended audience a direct way to complete that task, make the result easy to understand, and provide a useful next step. Start with one screen and one successful end-to-end journey. Use sample or non-sensitive data while shaping the experience, and validate the core behavior before adding optional sign-in, persistence, or production hosting.

## Proposed AWS workflow and architecture

The possible request flow is: **{flow_line}**. Treat this as a starting design to review against the final product requirements, data sensitivity, cost, and regional availability—not a deployment instruction.

{tailored_services}

In this flow, the user begins with the project's interface. The services above each have a specific role in supporting the request, data, or response; keep only those that are needed for the chosen first release. The suggestions are not resources created by Weekend Spark, and this project has not deployed the proposed architecture.

## How I would build it

First, build the main screen and make the core task work locally. Next, connect the first service in the proposed flow and verify one realistic request from beginning to end. Add any remaining listed services only when the user journey requires them, then test expected inputs, empty states, and an understandable failure path. For production, review least-privilege access, privacy, service limits, and cost before deployment.

## The delightful detail

The experience should make room for a small moment of delight: **{delight}**. This detail should make the result feel more useful without getting in the way of the main task. To evaluate it, ask a first-time person from the intended audience to try one realistic example. Observe whether they can finish the core task without coaching and whether the detail helps them understand or act on the result. This is a proposed test, not a claim that a study has already taken place.

## How this blueprint was made

Weekend Spark, the tool used to shape this proposal, is built with Python and Streamlit. Its local preview recommends AWS services from project needs using a rules-based planner. An optional Amazon Bedrock mode uses boto3 and Bedrock Runtime Converse to draft project-specific suggestions. This describes the blueprinting tool, not the proposed project architecture above.

## Proof it works

The screenshot at `assets/show-your-proof.png` shows Weekend Spark generating a project blueprint. It demonstrates the blueprinting interface, not a deployment or a completed implementation of {project}. Attach the screenshot or a short clip of the running prototype when publishing this article.

#add tags at the end.
"""
    return _article_word_limit(article)
