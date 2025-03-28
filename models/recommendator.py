def get_recommendation(face_shape):
    recommendations = {
        "Oval": {
            "hairstyle": "Layered cuts, pompadour, quiff",
            "beard": "Short boxed beard, stubble"
        },
        "Square": {
            "hairstyle": "Undercut, side part, buzz cut",
            "beard": "Circle beard, goatee"
        },
        "Round": {
            "hairstyle": "Spiky hair, faux hawk",
            "beard": "Extended goatee, anchor beard"
        },
        "Diamond": {
            "hairstyle": "Fringe, textured crop",
            "beard": "Full beard, chinstrap"
        },
        "Heart": {
            "hairstyle": "Side part, swept-back styles",
            "beard": "Light stubble, no beard"
        },
        "Rectangle (Oblong)": {
            "hairstyle": "Classic side part, medium-length styles",
            "beard": "Full beard to balance face"
        }
    }

    return recommendations.get(face_shape, {"hairstyle": "Unknown", "beard": "Unknown"})
