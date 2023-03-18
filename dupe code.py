@bot.slash_command(name="vdupe", description="Enables the venture dupe.")
async def vdupe(ctx):
    try:
        await ctx.defer()
        
        Account_Check = await user_data.find_one({"UserId": ctx.author.id})

        if Account_Check is None:
            await ctx.respond(embed=NotLoggedIn)
        else:

            items_dupeventure = []

            token_ref = Account_Check['AccessToken']
            accountid = Account_Check['AccountId']
            headers = {
                "Content-Type": f"application/json",
                "Authorization": f"Bearer {token_ref}"
            }
            data = json.dumps({})
            
            try:
                request = requests.post(f"https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/profile/" + accountid + "/client/QueryProfile?profileId=theater2&rvn=-1",headers=headers,data=data)
                res = request.json()
                
                stuff = res['profileChanges'][0]['profile']['items']
                
                for i in stuff:
                    if "building" in stuff[i]['templateId']:
                        items_dupeventure.append(i)
                        
                        
                if items_dupeventure == []:
                    embed = discord.Embed(title="`❌ Error ❌`", description="Dupe is Already ACTIVE",colour=discord.Colour.red())
                    await ctx.respond(embed=embed)
                else:
                    body = json.dumps({"itemIds": [items_dupeventure]})
                                   
                    requests.post(f"https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/profile/" + accountid + "/client/DestroyWorldItems?profileId=theater2&rvn=-1",headers=headers,data=body)
                    embed = discord.Embed(title="Successfully Enabled Ventures Dupe!",description=f"This is **IRREVERSIBLE** and the owner can do NOTHING about it.\n\n**`{Account_Check['DisplayName']}`**",colour=discord.Color.green())
                    await ctx.respond(embed=embed)
                    items_dupeventure.clear()
            except:
                await ctx.respond(embed=UnknownError)
    except:
        await ctx.respond(embed=UnknownError)