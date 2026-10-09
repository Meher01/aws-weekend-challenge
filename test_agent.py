import unittest
from pathlib import Path
from unittest.mock import patch

from agent import _article_word_limit, generate_article, generate_plan


class LocalAgentTests(unittest.TestCase):
    def setUp(self):
        self.brief = {
            "project_name": "Weekend Spark",
            "audience": "AWS builders",
            "problem": "scoping a small agent project",
            "delightful_detail": "celebrate a tiny next step",
        }

    def test_local_plan_uses_the_brief_and_is_honest_about_aws(self):
        plan = generate_plan(**self.brief)

        self.assertIn("Weekend Spark", plan)
        self.assertIn("celebrate a tiny next step", plan)
        self.assertIn("Suggested AWS services", plan)
        self.assertIn("not resources created by Spark", plan)

    def test_service_suggestions_follow_project_needs(self):
        brief = {
            "project_name": "Study Buddy",
            "audience": "students",
            "problem": "An AI assistant that answers questions from uploaded study documents, supports sign-in, and remembers user profiles.",
            "delightful_detail": "give a concise answer with a citation",
        }
        plan = generate_plan(**brief)

        self.assertIn("Amazon Bedrock", plan)
        self.assertIn("Amazon S3", plan)
        self.assertIn("Amazon Cognito", plan)
        self.assertIn("Amazon Bedrock Knowledge Bases", plan)
        self.assertIn("Possible architecture flow", plan)
        self.assertNotIn("Amazon RDS for PostgreSQL", plan)

    def test_local_article_meets_builder_center_word_count(self):
        plan = generate_plan(**self.brief)
        article = generate_article(self.brief, plan)

        self.assertGreaterEqual(len(article.split()), 500)
        self.assertIn("#agents", article)
        self.assertIn("Proof it works", article)
        self.assertIn("weekend-spark-proof.png", article)
        self.assertLessEqual(len(article.split()), 800)

    def test_article_is_based_on_the_idea_and_services(self):
        brief = {
            "project_name": "Study Buddy",
            "audience": "students",
            "problem": "An AI assistant that answers questions from uploaded study documents.",
            "delightful_detail": "give a concise answer with a citation",
        }
        plan = generate_plan(**brief)
        article = generate_article(brief, plan)

        self.assertTrue(article.startswith("# Study Buddy:"))
        self.assertNotIn("# Weekend Spark:", article)
        self.assertIn("## Project description", article)
        self.assertIn("## Proposed AWS workflow and architecture", article)
        self.assertIn("The possible request flow is:", article)
        self.assertIn("Amazon Bedrock", article)
        self.assertIn("Amazon S3", article)
        self.assertIn("Store uploaded files durably", article)
        self.assertLessEqual(len(article.split()), 800)
        self.assertGreaterEqual(len(article.split()), 500)

    def test_bedrock_article_prompt_requires_project_title_description_and_architecture(self):
        brief = {
            "project_name": "Study Buddy",
            "audience": "students",
            "problem": "An AI assistant that answers questions from uploaded study documents.",
            "delightful_detail": "give a concise answer with a citation",
        }
        with patch("agent._bedrock_text", return_value="# Study Buddy\n\n#agents") as mock_bedrock:
            article = generate_article(
                brief,
                "Possible architecture flow: User → Amazon S3 → Amazon Bedrock",
                use_bedrock=True,
                region="us-east-1",
                model_id="test-model",
            )

        prompt = mock_bedrock.call_args.args[0]
        self.assertIn("# A specific, engaging title about the user's project", prompt)
        self.assertIn("## Project description", prompt)
        self.assertIn("## Proposed AWS workflow and architecture", prompt)
        self.assertIn("Use only services from the supplied blueprint", prompt)
        self.assertIn("Amazon S3 → Amazon Bedrock", prompt)
        self.assertIn("#agents", article)

    def test_article_word_limit_preserves_required_tag(self):
        limited = _article_word_limit(("A complete sentence. " * 450).strip())

        self.assertLessEqual(len(limited.split()), 800)
        self.assertTrue(limited.endswith("#agents"))

    def test_publishable_article_file_has_required_sections_and_tag(self):
        article = (Path(__file__).parent / "article.md").read_text(encoding="utf-8")

        self.assertGreaterEqual(len(article.split()), 500)
        self.assertIn("What and who", article)
        self.assertIn("How I built it", article)
        self.assertIn("The delightful detail", article)
        self.assertIn("Proof it works", article)
        self.assertIn("#agents", article)

    def test_plan_rejects_incomplete_brief(self):
        with self.assertRaises(ValueError):
            generate_plan("Weekend Spark", "AWS builders", "", "one tiny next step")
