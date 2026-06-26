def validate_market(idea, competitors_count=5):
    """
    Returns True if idea has enough market demand based on competitors_count
    """
    # Example: reject ideas if too saturated
    if competitors_count > 20:
        return False
    return True

def filter_valid_ideas(ideas):
    return [idea for idea in ideas if validate_market(idea)]

if __name__ == "__main__":
    ideas = [{"name": "Test Idea 1"}, {"name": "Test Idea 2"}]
    print(filter_valid_ideas(ideas))
