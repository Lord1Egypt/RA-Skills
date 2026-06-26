def build_mvp(idea):
    """
    Creates a minimal viable product or landing page text
    """
    return {
        "landing_page": f"Launch {idea['name']} now and start generating revenue!",
        "call_to_action": "Sign up today and see results in 24 hours!"
    }

if __name__ == "__main__":
    idea = {"name": "Local Lead Generator"}
    print(build_mvp(idea))
