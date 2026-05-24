from app.schemas import VideoRequest


def generate_hashtags(product_name: str, target_audience: str, style: str, language: str):
    if language == "英文":
        hashtags = [
            "#TikTokShop",
            "#ProductReview",
            "#MustHave",
            "#TikTokMadeMeBuyIt",
            "#BestFinds",
            "#ShopNow"
        ]
    else:
        hashtags = [
            "#TikTokShop",
            "#带货视频",
            "#好物推荐",
            "#种草",
            "#实用好物",
            "#现在下单"
        ]

    hashtags.append("#" + product_name.replace(" ", ""))

    audience_map = {
        "上班": "#办公室好物",
        "学生": "#学生党好物",
        "宝妈": "#宝妈好物",
        "健身": "#健身好物",
        "旅行": "#旅行好物",
        "厨房": "#厨房好物",
        "宠物": "#宠物好物",
        "美妆": "#美妆好物",
    }

    for key, tag in audience_map.items():
        if key in target_audience:
            hashtags.append(tag)

    if "快节奏" in style:
        hashtags.append("#高转化短视频")
    if "测评" in style:
        hashtags.append("#真实测评")
    if "开箱" in style:
        hashtags.append("#开箱视频")

    result = []
    seen = set()
    for item in hashtags:
        if item not in seen:
            result.append(item)
            seen.add(item)
    return result


def generate_caption(product_name: str, target_audience: str, selling_points: str, price: str, language: str):
    if language == "英文":
        return (
            f"If you are {target_audience}, this {product_name} is worth checking out. "
            f"Key selling points: {selling_points}. "
            f"Price: {price}. Tap to shop now."
        )

    return (
        f"如果你是{target_audience}，这个{product_name}真的值得看看。\n"
        f"核心卖点：{selling_points}\n"
        f"价格：{price}\n"
        f"需要的话可以直接点小黄车。"
    )


def generate_title(req: VideoRequest):
    if req.template_type == "痛点带货":
        return f"还在忍这个麻烦？{req.product_name}可能就是解决方案"
    if req.template_type == "开箱测评":
        return f"{req.product_name}开箱实测：到底值不值得买？"
    if req.template_type == "对比测评":
        return f"{req.product_name}和普通款差在哪？对比给你看"
    if req.template_type == "口播种草":
        return f"我最近一直在用的{req.product_name}，真的想安利给你"
    return f"{req.product_name}真的有这么实用吗？"


def generate_hook(req: VideoRequest):
    p = req.product_name
    a = req.target_audience
    price = req.price

    if req.template_type == "痛点带货":
        return f"如果你总觉得某些小事很麻烦，那这个{p}你一定要看。"

    if req.template_type == "开箱测评":
        return f"{p}到底是不是智商税？我直接开箱给你看。"

    if req.template_type == "对比测评":
        return f"同样是{p}，为什么有的好用有的很鸡肋？"

    if req.template_type == "口播种草":
        return f"如果你是{a}，这个{p}我真的想推荐给你。"

    return f"{p}现在只要{price}，你先别急着划走。"


def generate_script_summary(req: VideoRequest):
    return (
        f"本条视频采用【{req.template_type}】模板，"
        f"围绕产品 {req.product_name} 面向 {req.target_audience} 展开，"
        f"核心突出卖点：{req.selling_points}，"
        f"并结合价格 {req.price} 做结尾转化。"
    )


def storyboard_pain_point(req: VideoRequest, hook: str):
    p = req.product_name
    a = req.target_audience
    s = req.selling_points
    price = req.price

    return [
        {
            "time": "0-3秒",
            "scene": "痛点开头",
            "visual": f"展示{a}在日常使用中的麻烦场景，节奏快。",
            "voiceover": hook,
            "subtitle": "你是不是也有这个烦恼？",
            "ai_prompt": f"TikTok vertical ad, daily inconvenience for {a}, fast-paced, emotional reaction, realistic lifestyle, 9:16"
        },
        {
            "time": "3-8秒",
            "scene": "产品出场",
            "visual": f"快速展示{p}外观和上手方式。",
            "voiceover": f"我最近发现这个{p}，用下来真的方便很多。",
            "subtitle": f"{p}出场",
            "ai_prompt": f"Product close-up of {p}, hands holding product, bright commercial lighting, TikTok Shop style, 9:16"
        },
        {
            "time": "8-16秒",
            "scene": "卖点展示",
            "visual": f"逐个展示核心卖点：{s}。",
            "voiceover": f"它最实用的地方就是：{s}。",
            "subtitle": s,
            "ai_prompt": f"Feature demonstration of {p}, showing {s}, realistic lifestyle usage, vertical 9:16"
        },
        {
            "time": "16-24秒",
            "scene": "使用场景",
            "visual": f"展示{a}在不同场景下使用产品。",
            "voiceover": f"不管是在家、办公室还是出门，用起来都很顺手。",
            "subtitle": "多场景都能用",
            "ai_prompt": f"User using {p} in home office outdoor scenes, happy expression, lifestyle TikTok ad, 9:16"
        },
        {
            "time": "24-30秒",
            "scene": "转化结尾",
            "visual": f"产品特写，画面叠加价格 {price} 和购买引导。",
            "voiceover": f"现在价格是{price}，如果你也需要，可以直接点小黄车。",
            "subtitle": f"{price}｜点小黄车",
            "ai_prompt": f"Hero shot of {p}, e-commerce layout, price overlay, call to action, TikTok Shop ad, 9:16"
        }
    ]


def storyboard_unboxing(req: VideoRequest, hook: str):
    p = req.product_name
    s = req.selling_points
    price = req.price

    return [
        {
            "time": "0-3秒",
            "scene": "开箱钩子",
            "visual": f"镜头快速扫过包装盒和产品外观，制造期待感。",
            "voiceover": hook,
            "subtitle": "开箱看看值不值",
            "ai_prompt": f"Unboxing scene of {p}, premium packaging, close-up, exciting TikTok opening, vertical 9:16"
        },
        {
            "time": "3-8秒",
            "scene": "外观展示",
            "visual": f"展示{p}的包装、尺寸、颜色、细节。",
            "voiceover": f"先看外观，整体设计还挺不错，拿在手上也很顺手。",
            "subtitle": "先看外观和细节",
            "ai_prompt": f"Detailed product beauty shot of {p}, clean background, realistic close-up, vertical 9:16"
        },
        {
            "time": "8-15秒",
            "scene": "功能体验",
            "visual": f"直接演示{p}的主要功能。",
            "voiceover": f"我实际试了一下，它的几个关键点是：{s}。",
            "subtitle": s,
            "ai_prompt": f"Hands-on demo of {p}, showing product function and key features: {s}, vertical 9:16"
        },
        {
            "time": "15-23秒",
            "scene": "真实评价",
            "visual": "展示产品使用效果和用户反应。",
            "voiceover": f"如果你更在意实用性，这个表现还是不错的，不是那种买回去就吃灰的类型。",
            "subtitle": "实测后：确实能用",
            "ai_prompt": f"Real user testing {p}, satisfied reaction, realistic review style, vertical 9:16"
        },
        {
            "time": "23-30秒",
            "scene": "结尾转化",
            "visual": f"产品特写+价格+引导下单。",
            "voiceover": f"现在到手大概{price}，想入手的话可以直接点链接看。",
            "subtitle": f"{price}｜想买点这里",
            "ai_prompt": f"Product hero shot of {p}, promotional layout, price and CTA, TikTok Shop ad, vertical 9:16"
        }
    ]


def storyboard_comparison(req: VideoRequest, hook: str):
    p = req.product_name
    s = req.selling_points
    price = req.price

    return [
        {
            "time": "0-3秒",
            "scene": "对比开头",
            "visual": f"左边普通款，右边{p}，做快速对比。",
            "voiceover": hook,
            "subtitle": "差别到底在哪？",
            "ai_prompt": f"Split screen comparison, regular product vs {p}, dramatic difference, TikTok style, vertical 9:16"
        },
        {
            "time": "3-8秒",
            "scene": "外观对比",
            "visual": "展示两者外观、体积、细节差异。",
            "voiceover": f"先看外观和细节，差别其实挺明显的。",
            "subtitle": "外观细节对比",
            "ai_prompt": f"Product comparison shot, design detail comparison, clean commercial setup, vertical 9:16"
        },
        {
            "time": "8-16秒",
            "scene": "功能对比",
            "visual": f"重点展示{p}在功能上的优势：{s}。",
            "voiceover": f"真正拉开差距的是使用体验，比如：{s}。",
            "subtitle": s,
            "ai_prompt": f"Feature comparison between normal version and {p}, product benefit demo, vertical 9:16"
        },
        {
            "time": "16-24秒",
            "scene": "结果对比",
            "visual": "展示使用后结果差异，突出效率或便利性。",
            "voiceover": f"用完之后你会发现，好不好用真的不是一点点差别。",
            "subtitle": "结果一眼看出来",
            "ai_prompt": f"Before after comparison, strong performance difference, TikTok ad style, vertical 9:16"
        },
        {
            "time": "24-30秒",
            "scene": "购买建议",
            "visual": f"{p}单独特写，叠加价格和建议。",
            "voiceover": f"如果你想一步到位，直接选这个更省事，现在价格{price}。",
            "subtitle": f"{price}｜一步到位更省心",
            "ai_prompt": f"Hero shot of {p}, premium e-commerce display, CTA and price overlay, vertical 9:16"
        }
    ]


def storyboard_talking(req: VideoRequest, hook: str):
    p = req.product_name
    a = req.target_audience
    s = req.selling_points
    price = req.price

    return [
        {
            "time": "0-4秒",
            "scene": "口播开头",
            "visual": "人物正对镜头口播，节奏直接。",
            "voiceover": hook,
            "subtitle": "真心想推荐给你",
            "ai_prompt": f"A creator speaking to camera recommending {p}, TikTok talking-head style, vertical 9:16"
        },
        {
            "time": "4-10秒",
            "scene": "适合人群",
            "visual": f"画面切到{a}的使用场景。",
            "voiceover": f"尤其如果你是{a}，我觉得这个东西会很实用。",
            "subtitle": f"特别适合：{a}",
            "ai_prompt": f"Lifestyle scene for {a} using {p}, realistic and warm, vertical 9:16"
        },
        {
            "time": "10-18秒",
            "scene": "卖点说明",
            "visual": f"边口播边展示产品细节和使用画面。",
            "voiceover": f"因为它有几个点真的很加分：{s}。",
            "subtitle": s,
            "ai_prompt": f"Talking head with product cutaways, showing {p}, feature highlights: {s}, TikTok style, 9:16"
        },
        {
            "time": "18-25秒",
            "scene": "真实感受",
            "visual": "用户使用后满意表情，展示生活提升感。",
            "voiceover": f"我自己用了一段时间，是真的那种会继续复购、继续推荐的类型。",
            "subtitle": "不是一时冲动买的",
            "ai_prompt": f"Happy user enjoying {p}, lifestyle improvement, realistic social content, vertical 9:16"
        },
        {
            "time": "25-30秒",
            "scene": "下单引导",
            "visual": f"产品特写+价格+CTA。",
            "voiceover": f"现在价格是{price}，你要是刚好需要，可以直接点链接看。",
            "subtitle": f"{price}｜需要就直接入",
            "ai_prompt": f"Product beauty shot of {p}, call to action, price tag, TikTok Shop ad, vertical 9:16"
        }
    ]


def generate_storyboard(req: VideoRequest, hook: str):
    if req.template_type == "痛点带货":
        return storyboard_pain_point(req, hook)
    if req.template_type == "开箱测评":
        return storyboard_unboxing(req, hook)
    if req.template_type == "对比测评":
        return storyboard_comparison(req, hook)
    if req.template_type == "口播种草":
        return storyboard_talking(req, hook)
    return storyboard_pain_point(req, hook)


def generate_tips(req: VideoRequest):
    base_tips = [
        "前 3 秒一定要先抓注意力，不要一上来就平铺直叙。",
        "字幕尽量短，一行不要太长。",
        "卖点最好控制在 3 个以内，方便观众记住。",
        "结尾一定要有明确 CTA，比如点小黄车、点链接、现在下单。"
    ]

    template_tips = {
        "痛点带货": "先讲麻烦，再给解决方案，最容易转化。",
        "开箱测评": "开箱类重点在真实感，不要太像硬广。",
        "对比测评": "对比类一定要让差异可视化，镜头要明显。",
        "口播种草": "口播类要像真人推荐，语气不要太官方。"
    }

    base_tips.append(template_tips.get(req.template_type, "根据目标用户调整表达。"))
    return base_tips


def generate_video_plan(req: VideoRequest):
    hook = generate_hook(req)
    storyboard = generate_storyboard(req, hook)

    return {
        "title": generate_title(req),
        "hook": hook,
        "script_summary": generate_script_summary(req),
        "template_type": req.template_type,
        "storyboard": storyboard,
        "caption": generate_caption(
            req.product_name,
            req.target_audience,
            req.selling_points,
            req.price,
            req.language
        ),
        "hashtags": generate_hashtags(
            req.product_name,
            req.target_audience,
            req.style,
            req.language
        ),
        "tips": generate_tips(req)
    }
