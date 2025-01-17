--Uses Medal Decompiler - github.com/centerepic/medal
--To use run Server.exe

local BetterDecompiler = {}

function BetterDecompiler.MedalDecompiler(Script)
    local HttpService = game:GetService("HttpService")
    local url = "http://localhost:3366/decompile"
    
    local bytecode = base64encode(getscriptbytecode(Script))

    local requestBody = {
        script = bytecode
    }
    
    local headers = {
        ["Content-Type"] = "application/json"
    }
    
    local jsonBody = HttpService:JSONEncode(requestBody)
    
    local success, response = pcall(function()
        local result = HttpService:RequestAsync({
            Url = url,
            Method = "POST",
            Headers = headers,
            Body = jsonBody
        })
        
        if result.Success and result.StatusCode == 200 then
            local resultData = HttpService:JSONDecode(result.Body)
            return resultData.fixed_script
        else
            warn("Request failed with status code: " .. (result.StatusCode or "unknown"))
            warn("Response body: " .. (result.Body or "no response body"))
        end
    end)
    
    if not success then
        warn("An error occurred: " .. response)
    end
    
    return base64.decode(Script)
end

function BetterDecompiler.decompile(scr)
    local success, srcScript = pcall(function()
        return BetterDecompiler.MedalDecompiler(scr)
    end)
        
    if not success then
        warn("Decompiler Error: " .. srcScript)
    end
    
    return srcScript
end

return BetterDecompiler.decompile
