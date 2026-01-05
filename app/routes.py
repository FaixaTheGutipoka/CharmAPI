# app/routes.py
import random
from fastapi import APIRouter, Query, Request, HTTPException
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.generator import SEED_DATA, get_seed_flirt, ai_generate_flirt

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

# Automatically fetch available contexts and tones from seed data
CONTEXTS = list(SEED_DATA.keys())
TONES = list({tone for ctx in SEED_DATA.values() for tone in ctx.keys()})

@router.get("/flirt")
@limiter.limit("120/minute")
def flirt(
    request: Request,
    context: str | None = Query(None),
    tone: str | None = Query(None),
    use_seed: bool | None = None
):
    # Pick random context/tone if not specified
    if context is None:
        context = random.choice(CONTEXTS)
    elif context not in CONTEXTS:
        raise HTTPException(status_code=400, detail=f"Invalid context. Choose from: {CONTEXTS}")

    if tone is None:
        tone = random.choice(list(SEED_DATA[context].keys()))
    elif tone not in SEED_DATA.get(context, {}):
        raise HTTPException(status_code=400, detail=f"Invalid tone for context '{context}'. Choose from: {list(SEED_DATA[context].keys())}")

    # Decide randomly whether to use AI or seed if use_seed not specified
    if use_seed is None:
        use_seed = random.choices([False, True], weights=[50, 50])[0]  # 50% AI, 50% seed

    # Get flirt line
    if not use_seed:
        try:
            flirt_line = ai_generate_flirt(context, tone)
            source = "ai"
        except Exception as e:
            print(f"[Fallback to seed] AI error: {e}")
            flirt_line = get_seed_flirt(context, tone)
            source = "seed"
    else:
        flirt_line = get_seed_flirt(context, tone)
        source = "seed"

    return {
        "flirt": flirt_line,
        "context": context,
        "tone": tone,
        "source": source
    }

@router.get("/flirt/random")
def random_flirt():
    # Fully random flirt
    context = random.choice(CONTEXTS)
    tone = random.choice(list(SEED_DATA[context].keys()))
    use_seed = random.choices([False, True], weights=[50, 50])[0]

    if not use_seed:
        try:
            flirt_line = ai_generate_flirt(context, tone)
            source = "ai"
        except Exception as e:
            print(f"[Fallback to seed] AI error: {e}")
            flirt_line = get_seed_flirt(context, tone)
            source = "seed"
    else:
        flirt_line = get_seed_flirt(context, tone)
        source = "seed"

    return {
        "flirt": flirt_line,
        "context": context,
        "tone": tone,
        "source": source
    }
