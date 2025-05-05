
from store import Store, StoreException
import random

def get_score(store, phone, email, birthday=None, gender=None, first_name=None, last_name=None):
    key = f"score:{phone or ''}:{email or ''}"
    score = None
    if store:
        score = store.cache_get(key)
        if score is not None:
            try:
                return float(score)
            except ValueError:
                pass
    score = 0
    if phone:
        score += 1.5
    if email:
        score += 1.5
    if birthday and gender is not None:
        score += 1.5
    if first_name and last_name:
        score += 0.5
    if store:
        try:
            store.set(key, score, ex=60)
        except Exception:
            pass
    return score

def get_interests(store, cid):
    key = f"i:{cid}"
    if not store:
        raise StoreException("Store not available")
    try:
        interests = store.get(key)
        if interests:
            return interests.split(",")
    except Exception as e:
        raise StoreException("Failed to fetch interests") from e
    raise StoreException("No interests found")
