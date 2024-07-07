class FoodItem:
    def __init__(self, name, category, calories, protein, carbs, fat):
        self.name = name
        self.category = category
        self.calories = calories
        self.protein = protein
        self.carbs = carbs
        self.fat = fat

class UserProfile:
    def __init__(self, name, age, gender, dietaryRestrictions, goals, healthConditions):
        self.name = name
        self.age = age
        self.gender = gender
        self.dietaryRestrictions = dietaryRestrictions
        self.goals = goals
        self.healthConditions = healthConditions

class HealthConditions:
    def __init__(self, hasDiabetes, hasHighBloodPressure):
        self.hasDiabetes = hasDiabetes
        self.hasHighBloodPressure = hasHighBloodPressure


class DietaryRestrictions:
    def __init__(self, isPeanutAllergic, isDiaryAllergic):
        self.isPeanutAllergic = isPeanutAllergic
        self.isDiaryAllergic = isDiaryAllergic


class FitnessGoals:
    def __init__(self, isBuildMuscle, isLoseWeight):
        self.isBuildMuscle = isBuildMuscle
        self.isLoseWeight = isLoseWeight

def calculateScore(userProfile, foodItem):

    # step 1: dietary restriction
    if userProfile.dietaryRestrictions.isPeanutAllergic and foodItem.category.lower() == "peanut":
        return 0.0

    # step 2: nutrient density
    nutrient_density = calculate_nutrient_density(foodItem)
    print(nutrient_density)

    # step 3: user goal
    weights = calculate_weights_based_on_goals(userProfile.goals)
    print(weights)

    # step 4: health conditions
    weights = adjust_weights_for_health_conditions(weights, userProfile.healthConditions)
    print(weights)

    single_score = sum(nutrient_density[category] * weight for category, weight in weights.items())

    # Normalize the score to be out of 100
    single_score_out_of_100 = single_score * 10  # Since scores are out of 10
    print(single_score_out_of_100)

    return single_score_out_of_100


def calculate_nutrient_density(foodItem):
    # Define thresholds for scoring
    calorie_threshold = 100  # Example: 100 calories per serving is considered low
    carb_threshold = 20      # Example: 20 grams of carbs per serving
    protein_threshold = 10   # Example: 10 grams of protein per serving
    fat_threshold = 10       # Example: 10 grams of fat per serving

    # Calculate scores based on thresholds
    calorie_score = max(0, min(10, 10 - (foodItem.calories / calorie_threshold * 10)))
    carb_score = max(0, min(10, 10 - (foodItem.carbs / carb_threshold * 10)))
    protein_score = max(0, min(10, foodItem.protein / protein_threshold * 10))
    fat_score = max(0, min(10, 10 - (foodItem.fat / fat_threshold * 10)))

    return {
        'calorie_score': calorie_score,
        'carb_score': carb_score,
        'protein_score': protein_score,
        'fat_score': fat_score
    }

def calculate_weights_based_on_goals(fitness_goals):
    # Base weights
    weights = {
        'calorie_score': 0.25,
        'carb_score': 0.25,
        'protein_score': 0.25,
        'fat_score': 0.25
    }

    if fitness_goals.isBuildMuscle and fitness_goals.isLoseWeight:
        # Balance weights for both goals
        weights['calorie_score'] = 0.25
        weights['carb_score'] = 0.15
        weights['protein_score'] = 0.4
        weights['fat_score'] = 0.2
    elif fitness_goals.isBuildMuscle:
        # Emphasize protein for muscle building
        weights['calorie_score'] = 0.2
        weights['carb_score'] = 0.2
        weights['protein_score'] = 0.4
        weights['fat_score'] = 0.2
    elif fitness_goals.isLoseWeight:
        # Emphasize calories and fat for weight loss
        weights['calorie_score'] = 0.35
        weights['carb_score'] = 0.2
        weights['protein_score'] = 0.2
        weights['fat_score'] = 0.25

    return weights

def adjust_weights_for_health_conditions(weights, health_conditions):
    if health_conditions.hasDiabetes:
        weights['carb_score'] *= 1.2
        weights['fat_score'] *= 0.8
        weights['protein_score'] *= 1.1

    if health_conditions.hasHighBloodPressure:
        weights['fat_score'] *= 0.8
        weights['protein_score'] *= 1.1

    # Normalize weights to sum up to 1
    total_weight = sum(weights.values())
    weights = {key: value / total_weight for key, value in weights.items()}

    return weights

# Example Usage:
if __name__ == "__main__":

    # Create some food items
    apple = FoodItem("Apple", "Fruit", 52, 19, 4, 2)
    burger = FoodItem("Burger", "Fast Food", 295, 0, 26, 34)
    
    # Create a user profile
    user = UserProfile("John Doe", 30, "M", DietaryRestrictions(0, 0), FitnessGoals(0, 1), HealthConditions(0, 1))

    score = calculateScore(user, apple)
    
